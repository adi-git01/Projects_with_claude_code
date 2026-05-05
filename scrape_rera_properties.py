"""
RERA Karnataka Property Scraper
Scrapes project details for Bengaluru Urban & South Bengaluru districts
filtered by promoter type "Kreta" from https://rera.karnataka.gov.in/projectViewDetails

Run:  python3 scrape_rera_properties.py
Output: rera_properties.csv
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import sys
import re
import json
from urllib.parse import urljoin


BASE_URL = "https://rera.karnataka.gov.in"
SEARCH_URL = f"{BASE_URL}/projectViewDetails"

# District name -> district ID mapping (from the site's dropdown)
# These IDs are discovered at runtime; fallback values are provided below.
DISTRICT_NAME_HINTS = ["Bengaluru Urban", "Bangalore Urban", "South Bengaluru", "Bangalore South"]

# Promoter type filter keyword
KRETA_KEYWORD = "kreta"

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
    "Referer": BASE_URL,
}


def make_session():
    s = requests.Session()
    s.headers.update(HEADERS)
    return s


def load_search_page(session):
    """GET the search page; returns BeautifulSoup and raw response."""
    print("[*] Loading search page ...")
    r = session.get(SEARCH_URL, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "lxml")
    return soup, r


def discover_form_fields(soup):
    """
    Inspect the search form to extract:
      - All <select> / <input> field names and their option values
      - CSRF / hidden tokens
    Returns a dict: { field_name: {label, options: [(value, text), ...]} }
    """
    form = soup.find("form")
    if not form:
        # Try to find any form-like structure
        forms = soup.find_all("form")
        print(f"[!] Found {len(forms)} form(s) on the page.")
        if forms:
            form = forms[0]

    fields = {}

    if form:
        # Hidden inputs (CSRF tokens, etc.)
        for inp in form.find_all("input"):
            name = inp.get("name", "")
            val = inp.get("value", "")
            itype = inp.get("type", "text")
            if name:
                fields[name] = {"type": itype, "default": val, "options": [(val, val)]}

        # Select dropdowns
        for sel in form.find_all("select"):
            name = sel.get("name", "")
            if not name:
                continue
            options = []
            for opt in sel.find_all("option"):
                v = opt.get("value", "").strip()
                t = opt.get_text(strip=True)
                options.append((v, t))
            fields[name] = {"type": "select", "default": "", "options": options}

    return fields


def find_district_ids(fields):
    """
    Scan select fields for options matching our target districts.
    Returns list of (field_name, value, display_text) tuples.
    """
    targets = []
    for fname, fdata in fields.items():
        if fdata["type"] != "select":
            continue
        for val, text in fdata["options"]:
            for hint in DISTRICT_NAME_HINTS:
                if hint.lower() in text.lower():
                    targets.append((fname, val, text))
                    break
    return targets


def find_kreta_option(fields):
    """
    Look for a 'kreta' option in any select field (promoter type, applicant type, etc.)
    Returns (field_name, value) or (None, None).
    """
    for fname, fdata in fields.items():
        if fdata["type"] != "select":
            continue
        for val, text in fdata["options"]:
            if KRETA_KEYWORD in text.lower():
                return fname, val
    return None, None


def build_post_data(fields, district_field, district_val, kreta_field=None, kreta_val=None, page=1):
    """Construct the POST body for a search request."""
    data = {}
    # Include all hidden/default fields
    for fname, fdata in fields.items():
        if fdata["type"] in ("hidden", "text", "radio", "checkbox"):
            data[fname] = fdata["default"]

    # Set district
    data[district_field] = district_val

    # Set kreta filter if found
    if kreta_field and kreta_val:
        data[kreta_field] = kreta_val

    # Common pagination field names used by government portals
    for pg_field in ("page", "pageNo", "pageNumber", "currentPage", "draw"):
        if pg_field in fields:
            data[pg_field] = page

    return data


def parse_results_table(soup):
    """
    Parse project rows from the results table.
    Returns list of dicts.
    """
    rows_data = []

    # Try to find the main data table
    tables = soup.find_all("table")
    if not tables:
        return rows_data

    # Pick the table with the most rows (likely the data table)
    best_table = max(tables, key=lambda t: len(t.find_all("tr")))
    rows = best_table.find_all("tr")

    if not rows:
        return rows_data

    # Extract headers from first row
    header_row = rows[0]
    headers = [th.get_text(strip=True) for th in header_row.find_all(["th", "td"])]
    if not headers:
        return rows_data

    # Extract data rows
    for row in rows[1:]:
        cells = row.find_all(["td", "th"])
        if not cells:
            continue
        record = {}
        for i, cell in enumerate(cells):
            key = headers[i] if i < len(headers) else f"col_{i}"
            # Also capture any links inside the cell
            link = cell.find("a")
            record[key] = cell.get_text(strip=True)
            if link and link.get("href"):
                record[f"{key}_url"] = urljoin(BASE_URL, link["href"])
        rows_data.append(record)

    return rows_data


def get_total_pages(soup):
    """
    Detect pagination info from common patterns used in gov portals.
    Returns total_pages (int), defaults to 1 if not found.
    """
    # Pattern: "Showing X to Y of Z entries"
    text = soup.get_text()
    m = re.search(r"(\d[\d,]*)\s+(?:entries|records|results)", text, re.IGNORECASE)
    if m:
        total = int(m.group(1).replace(",", ""))
        rows_per_page = 10  # common default
        return max(1, -(-total // rows_per_page))  # ceiling division

    # Pattern: pagination links
    pag = soup.find_all("a", string=re.compile(r"^\d+$"))
    if pag:
        nums = [int(a.get_text(strip=True)) for a in pag]
        return max(nums) if nums else 1

    # DataTables JSON pattern
    dt_match = re.search(r'"recordsTotal"\s*:\s*(\d+)', text)
    if dt_match:
        total = int(dt_match.group(1))
        return max(1, -(-total // 10))

    return 1


def scrape_district(session, fields, district_field, district_val, district_name,
                    kreta_field=None, kreta_val=None):
    """Scrape all pages for a given district."""
    all_records = []
    page = 1

    while True:
        print(f"  [*] District: {district_name}  |  Page {page} ...")
        post_data = build_post_data(
            fields, district_field, district_val, kreta_field, kreta_val, page
        )

        try:
            r = session.post(SEARCH_URL, data=post_data, timeout=30)
            r.raise_for_status()
        except requests.RequestException as e:
            print(f"  [!] Request error on page {page}: {e}")
            break

        soup = BeautifulSoup(r.text, "lxml")
        records = parse_results_table(soup)

        if not records:
            print(f"  [*] No records on page {page}. Stopping.")
            break

        # Stamp source info
        for rec in records:
            rec["_district"] = district_name
            rec["_page"] = page

        all_records.extend(records)
        print(f"      -> {len(records)} records found (total so far: {len(all_records)})")

        total_pages = get_total_pages(soup)
        if page >= total_pages:
            break

        page += 1
        time.sleep(1.5)  # polite delay between requests

    return all_records


def try_ajax_endpoint(session, soup, district_ids, kreta_field, kreta_val):
    """
    Some government portals load results via DataTables AJAX.
    Try to detect and call the AJAX endpoint directly.
    Returns records list or None if not applicable.
    """
    text = soup.get_text()
    # Look for DataTables server-side URL in the page source
    src = str(soup)
    ajax_url_match = re.search(r'["\']url["\']\s*:\s*["\'](/[^"\']+)["\']', src)
    if ajax_url_match:
        ajax_path = ajax_url_match.group(1)
        print(f"[*] Detected AJAX endpoint: {ajax_path}")
        return ajax_path
    return None


def main():
    session = make_session()

    # Step 1: Load the search page
    try:
        soup, _ = load_search_page(session)
    except Exception as e:
        print(f"[ERROR] Cannot reach {SEARCH_URL}: {e}")
        print("        Make sure you are running this on a machine with access to the site.")
        sys.exit(1)

    print("[*] Page loaded. Discovering form fields ...")
    fields = discover_form_fields(soup)

    if not fields:
        print("[!] No form fields found. The page may require JavaScript (try Selenium mode).")
        # Still attempt to parse any table that's already on the page
    else:
        print(f"[*] Found {len(fields)} form fields: {', '.join(fields.keys())}")

    # Step 2: Identify district options
    district_targets = find_district_ids(fields)
    if not district_targets:
        print("[!] Could not auto-detect district IDs. Dumping all select options for inspection:")
        for fname, fdata in fields.items():
            if fdata["type"] == "select":
                print(f"    Field '{fname}':")
                for val, text in fdata["options"]:
                    print(f"      value={val!r:20s}  text={text!r}")
        sys.exit(1)

    print(f"[*] Target districts found: {[(t[2]) for t in district_targets]}")

    # Step 3: Identify kreta filter
    kreta_field, kreta_val = find_kreta_option(fields)
    if kreta_field:
        print(f"[*] Kreta filter: field='{kreta_field}', value='{kreta_val}'")
    else:
        print("[!] No 'kreta' option found in any dropdown. Will scrape without that filter.")
        print("    Available options (check manually):")
        for fname, fdata in fields.items():
            if fdata["type"] == "select":
                for val, text in fdata["options"]:
                    print(f"      [{fname}] {val!r} -> {text!r}")

    # Step 4: Scrape each target district
    all_records = []
    seen_districts = set()

    for district_field, district_val, district_name in district_targets:
        key = (district_field, district_val)
        if key in seen_districts:
            continue
        seen_districts.add(key)

        records = scrape_district(
            session, fields, district_field, district_val, district_name,
            kreta_field, kreta_val
        )
        all_records.extend(records)

    # Step 5: Save to CSV
    if not all_records:
        print("[!] No records collected. Check the site structure or run in Selenium mode.")
        sys.exit(1)

    df = pd.DataFrame(all_records)
    # Drop internal tracking columns from the visible output order but keep them
    out_path = "rera_properties.csv"
    df.to_csv(out_path, index=False, encoding="utf-8-sig")
    print(f"\n[+] Done! {len(df)} records saved to {out_path}")
    print(df.head())


if __name__ == "__main__":
    main()
