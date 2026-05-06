"""
RERA Karnataka Property Scraper
Scrapes project details for Bengaluru Urban & South Bengaluru districts
filtered by promoter type "Kreta" from https://rera.karnataka.gov.in/projectViewDetails

Run:        python3 scrape_rera_properties.py
Diagnose:   python3 scrape_rera_properties.py --diagnose
Output:     rera_properties.csv
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import sys
import re
import json
import argparse
from urllib.parse import urljoin, urlparse

BASE_URL = "https://rera.karnataka.gov.in"
POST_URL = f"{BASE_URL}/projectViewDetails"

DISTRICT_NAME_HINTS = [
    "bengaluru urban", "bangalore urban",
    "south bengaluru", "bangalore south",
    "bengaluru south", "south bangalore",
    "bbmp south",
]
KRETA_KEYWORD = "kreta"

# Candidate pages that might host the search form
FORM_CANDIDATE_URLS = [
    f"{BASE_URL}/home",
    f"{BASE_URL}/",
    f"{BASE_URL}/home?language=en",
    f"{BASE_URL}/projectViewDetails",   # some sites serve form on GET too
    f"{BASE_URL}/viewAllProjects?language=en",
    f"{BASE_URL}/viewProjects",
    f"{BASE_URL}/searchProject",
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}


# ── helpers ──────────────────────────────────────────────────────────────────

def make_session():
    s = requests.Session()
    s.headers.update(HEADERS)
    return s


def try_get(session, url, timeout=30):
    """GET url; return (soup, response) or (None, None) on error."""
    try:
        r = session.get(url, timeout=timeout, allow_redirects=True)
        print(f"    GET {url}  ->  HTTP {r.status_code}")
        if r.status_code == 200 and r.text.strip():
            return BeautifulSoup(r.text, "lxml"), r
    except Exception as e:
        print(f"    GET {url}  ->  ERROR: {e}")
    return None, None


def extract_forms(soup, page_url):
    """Return list of all <form> elements found in soup."""
    return soup.find_all("form") if soup else []


def parse_form(form, page_url):
    """
    Extract all fields from a <form> element.
    Returns dict: { field_name: {type, default, options} }
    """
    fields = {}
    action = form.get("action", "")
    method = form.get("method", "get").lower()

    for inp in form.find_all("input"):
        name = inp.get("name", "").strip()
        if not name:
            continue
        itype = inp.get("type", "text").lower()
        val = inp.get("value", "")
        fields[name] = {"type": itype, "default": val, "options": [(val, val)]}

    for sel in form.find_all("select"):
        name = sel.get("name", "").strip()
        if not name:
            continue
        options = []
        for opt in sel.find_all("option"):
            v = opt.get("value", "").strip()
            t = opt.get_text(strip=True)
            options.append((v, t))
        fields[name] = {"type": "select", "default": "", "options": options}

    for ta in form.find_all("textarea"):
        name = ta.get("name", "").strip()
        if not name:
            continue
        fields[name] = {"type": "textarea", "default": ta.get_text(), "options": []}

    return {
        "action": urljoin(page_url, action) if action else POST_URL,
        "method": method,
        "fields": fields,
    }


def find_best_form(session, diagnose=False):
    """
    Try each candidate page until we find a form with a district <select>.
    Returns parsed form dict or None.
    """
    for url in FORM_CANDIDATE_URLS:
        soup, resp = try_get(session, url)
        if soup is None:
            continue

        if diagnose:
            slug = url.replace("https://", "").replace("/", "_").replace("?", "_").replace("=", "_")
            fname = f"diagnose_{slug}.html"
            with open(fname, "w", encoding="utf-8") as f:
                f.write(resp.text)
            print(f"    [diagnose] saved raw HTML -> {fname}")

        forms = extract_forms(soup, url)
        print(f"    Found {len(forms)} form(s) on {url}")

        for form in forms:
            parsed = parse_form(form, url)
            fields = parsed["fields"]
            # Check if any select has district-like options
            for fname_f, fdata in fields.items():
                if fdata["type"] == "select":
                    for val, text in fdata["options"]:
                        if any(h in text.lower() for h in DISTRICT_NAME_HINTS):
                            print(f"    -> District select found in form (action={parsed['action']})")
                            return parsed, soup, resp

        # Even if no district select, keep the first successful page's form
        # so we can do a POST probe — store as fallback
        if forms and 'fallback' not in dir():
            fallback_parsed = parse_form(forms[0], url)
            fallback_soup = soup
            fallback_resp = resp

    # Return fallback if we found any form at all
    try:
        return fallback_parsed, fallback_soup, fallback_resp
    except NameError:
        return None, None, None


# ── district / kreta detection ────────────────────────────────────────────────

def find_district_ids(fields):
    targets = []
    for fname, fdata in fields.items():
        if fdata["type"] != "select":
            continue
        for val, text in fdata["options"]:
            for hint in DISTRICT_NAME_HINTS:
                if hint in text.lower() and val:
                    targets.append((fname, val, text))
                    break
    return targets


def find_kreta_option(fields):
    for fname, fdata in fields.items():
        if fdata["type"] != "select":
            continue
        for val, text in fdata["options"]:
            if KRETA_KEYWORD in text.lower() and val:
                return fname, val
    return None, None


def dump_all_selects(fields):
    print("\n  All <select> fields and their options:")
    for fname, fdata in fields.items():
        if fdata["type"] == "select":
            print(f"    [{fname}]")
            for val, text in fdata["options"]:
                print(f"      {val!r:30s}  {text!r}")


# ── POST / results parsing ────────────────────────────────────────────────────

def build_post_data(fields, district_field, district_val,
                    kreta_field=None, kreta_val=None, page=1):
    data = {}
    for fname, fdata in fields.items():
        if fdata["type"] in ("hidden",):
            data[fname] = fdata["default"]
    data[district_field] = district_val
    if kreta_field and kreta_val:
        data[kreta_field] = kreta_val
    for pg_field in ("page", "pageNo", "pageNumber", "currentPage", "draw", "start"):
        if pg_field in fields:
            data[pg_field] = (page - 1) * 10 if pg_field == "start" else page
    return data


def parse_results_table(soup):
    rows_data = []
    tables = soup.find_all("table")
    if not tables:
        return rows_data
    best_table = max(tables, key=lambda t: len(t.find_all("tr")))
    rows = best_table.find_all("tr")
    if len(rows) < 2:
        return rows_data
    header_row = rows[0]
    headers = [th.get_text(strip=True) for th in header_row.find_all(["th", "td"])]
    if not headers:
        return rows_data
    for row in rows[1:]:
        cells = row.find_all(["td", "th"])
        if not cells:
            continue
        record = {}
        for i, cell in enumerate(cells):
            key = headers[i] if i < len(headers) else f"col_{i}"
            record[key] = cell.get_text(strip=True)
            link = cell.find("a")
            if link and link.get("href"):
                record[f"{key}_url"] = urljoin(BASE_URL, link["href"])
        rows_data.append(record)
    return rows_data


def get_total_pages(soup):
    text = soup.get_text()
    # "X of Y entries" or "Y records"
    for pat in [
        r"of\s+([\d,]+)\s+(?:entries|records|results)",
        r"Total\s*:?\s*([\d,]+)",
        r"([\d,]+)\s+(?:entries|records|results)\s+found",
    ]:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            total = int(m.group(1).replace(",", ""))
            return max(1, -(-total // 10))
    # DataTables JSON in page source
    dt = re.search(r'"recordsTotal"\s*:\s*(\d+)', str(soup))
    if dt:
        return max(1, -(-int(dt.group(1)) // 10))
    # Numbered pagination links
    nums = [int(a.get_text(strip=True))
            for a in soup.find_all("a", string=re.compile(r"^\d+$"))]
    return max(nums) if nums else 1


def do_post(session, action_url, post_data, referer, diagnose=False, page=1):
    """POST search form; return (soup, response) or raise."""
    hdrs = {"Referer": referer, "Origin": BASE_URL,
            "Content-Type": "application/x-www-form-urlencoded"}
    r = session.post(action_url, data=post_data, headers=hdrs, timeout=30)
    print(f"    POST {action_url}  ->  HTTP {r.status_code}  ({len(r.text)} bytes)")
    if diagnose:
        with open(f"diagnose_post_page{page}.html", "w", encoding="utf-8") as f:
            f.write(r.text)
        print(f"    [diagnose] saved POST response -> diagnose_post_page{page}.html")
    r.raise_for_status()
    return BeautifulSoup(r.text, "lxml"), r


def scrape_district(session, form, district_field, district_val, district_name,
                    kreta_field, kreta_val, form_page_url, diagnose=False):
    all_records = []
    fields = form["fields"]
    action = form["action"]
    page = 1

    while True:
        print(f"  [*] {district_name}  |  Page {page} ...")
        post_data = build_post_data(fields, district_field, district_val,
                                    kreta_field, kreta_val, page)
        try:
            soup, _ = do_post(session, action, post_data, form_page_url,
                              diagnose=diagnose, page=page)
        except requests.HTTPError as e:
            print(f"  [!] HTTP error on page {page}: {e}")
            break
        except Exception as e:
            print(f"  [!] Error on page {page}: {e}")
            break

        records = parse_results_table(soup)
        if not records:
            print(f"  [*] No records on page {page}. Stopping.")
            break

        for rec in records:
            rec["_district"] = district_name
            rec["_page"] = page
        all_records.extend(records)
        print(f"      -> {len(records)} rows  (total: {len(all_records)})")

        total_pages = get_total_pages(soup)
        if page >= total_pages:
            break
        page += 1
        time.sleep(1.5)

    return all_records


# ── main ─────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--diagnose", action="store_true",
                    help="Save raw HTML of every request for debugging")
    args = ap.parse_args()

    session = make_session()

    print("[*] Searching for the project search form ...")
    form, form_soup, form_resp = find_best_form(session, diagnose=args.diagnose)

    if form is None:
        print("\n[ERROR] Could not load any page from rera.karnataka.gov.in.")
        print("  - Check your internet connection.")
        print("  - Try opening https://rera.karnataka.gov.in/home in a browser.")
        sys.exit(1)

    fields = form["fields"]
    action = form["action"]
    form_page_url = form_resp.url if form_resp else BASE_URL
    print(f"\n[*] Form found. Action URL: {action}")
    print(f"[*] {len(fields)} field(s): {', '.join(fields.keys())}")

    # District discovery
    district_targets = find_district_ids(fields)
    if not district_targets:
        print("\n[!] No Bengaluru Urban / South Bengaluru districts found in any dropdown.")
        dump_all_selects(fields)
        if not args.diagnose:
            print("\n  Tip: run with --diagnose to save raw HTML for inspection.")
        sys.exit(1)

    # Remove duplicates
    seen, unique_targets = set(), []
    for t in district_targets:
        key = (t[0], t[1])
        if key not in seen:
            seen.add(key)
            unique_targets.append(t)

    print(f"[*] Target districts: {[t[2] for t in unique_targets]}")

    # Kreta filter discovery
    kreta_field, kreta_val = find_kreta_option(fields)
    if kreta_field:
        print(f"[*] Kreta filter: [{kreta_field}] = {kreta_val!r}")
    else:
        print("[!] No 'kreta' option found — scraping all promoter types.")
        if args.diagnose:
            dump_all_selects(fields)

    # Scrape
    all_records = []
    for district_field, district_val, district_name in unique_targets:
        print(f"\n[>] Scraping: {district_name}")
        records = scrape_district(
            session, form, district_field, district_val, district_name,
            kreta_field, kreta_val, form_page_url, diagnose=args.diagnose
        )
        all_records.extend(records)

    if not all_records:
        print("\n[!] No records collected.")
        if not args.diagnose:
            print("  Run with --diagnose to save HTML dumps for inspection.")
        sys.exit(1)

    df = pd.DataFrame(all_records)
    out_path = "rera_properties.csv"
    df.to_csv(out_path, index=False, encoding="utf-8-sig")
    print(f"\n[+] {len(df)} records saved to {out_path}")
    print(df.head(3).to_string())


if __name__ == "__main__":
    main()
