"""
RERA Karnataka Property Scraper — Selenium version
Handles JavaScript-rendered pages.

Requirements:
    pip install selenium webdriver-manager pandas

Run:
    python3 scrape_rera_selenium.py
    python3 scrape_rera_selenium.py --show-browser      # visible window
    python3 scrape_rera_selenium.py --diagnose           # save HTML dumps

Output:
    rera_properties.csv
"""

import time
import re
import sys
import os
import argparse
import pandas as pd

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import Select, WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options as ChromeOptions
    from selenium.webdriver.firefox.options import Options as FirefoxOptions
    from selenium.common.exceptions import (
        NoSuchElementException, TimeoutException, StaleElementReferenceException
    )
except ImportError:
    print("[ERROR] selenium not installed. Run: pip install selenium")
    sys.exit(1)

BASE_URL = "https://rera.karnataka.gov.in"
HOME_URL = f"{BASE_URL}/home"

DISTRICT_HINTS = [
    "bengaluru urban", "bangalore urban",
    "south bengaluru", "bangalore south",
    "bengaluru south", "south bangalore",
]
KRETA_HINTS = ["kreta", "buyer", "purchaser"]

# If JS renders the dropdowns lazily, how long to wait (seconds)
PAGE_WAIT = 8
POLL_INTERVAL = 0.5


# ── driver setup ─────────────────────────────────────────────────────────────

def make_driver(headless=True):
    for browser in ("chrome", "firefox"):
        try:
            if browser == "chrome":
                opts = ChromeOptions()
                if headless:
                    opts.add_argument("--headless=new")
                opts.add_argument("--no-sandbox")
                opts.add_argument("--disable-dev-shm-usage")
                opts.add_argument("--window-size=1400,900")
                opts.add_argument("--disable-blink-features=AutomationControlled")
                opts.add_experimental_option("excludeSwitches", ["enable-automation"])
                opts.add_argument(
                    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36"
                )
                driver = webdriver.Chrome(options=opts)
            else:
                opts = FirefoxOptions()
                if headless:
                    opts.add_argument("--headless")
                driver = webdriver.Firefox(options=opts)
            print(f"[*] Using {browser.capitalize()} WebDriver")
            return driver
        except Exception as e:
            print(f"[!] {browser.capitalize()} failed: {e}")
    print("[ERROR] No browser available. Install Chrome or Firefox.")
    sys.exit(1)


# ── page interaction helpers ──────────────────────────────────────────────────

def wait_for_selects(driver, min_count=1, timeout=PAGE_WAIT):
    """Wait until at least min_count <select> elements are present."""
    end = time.time() + timeout
    while time.time() < end:
        sels = driver.find_elements(By.TAG_NAME, "select")
        if len(sels) >= min_count:
            return sels
        time.sleep(POLL_INTERVAL)
    return driver.find_elements(By.TAG_NAME, "select")


def get_options(driver, select_el):
    try:
        sel = Select(select_el)
        return [(o.get_attribute("value") or "", o.text.strip()) for o in sel.options]
    except Exception:
        return []


def save_html(driver, filename):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    print(f"    [diagnose] saved -> {filename}")


def find_project_search_link(driver):
    """
    The search form may not be at the root URL. Try to find a nav link
    that leads to the project search/view page.
    """
    keywords = ["project", "view project", "search project", "registered project"]
    links = driver.find_elements(By.TAG_NAME, "a")
    for link in links:
        text = link.text.strip().lower()
        href = (link.get_attribute("href") or "").lower()
        for kw in keywords:
            if kw in text or kw.replace(" ", "") in href:
                return link
    return None


def navigate_to_search_form(driver, diagnose=False):
    """
    Load the home page, navigate to the project search section,
    and wait for the search form with dropdowns to appear.
    Returns the URL of the search form page, or None on failure.
    """
    print(f"[*] Loading {HOME_URL} ...")
    driver.get(HOME_URL)
    time.sleep(3)

    if diagnose:
        save_html(driver, "diagnose_home.html")

    # Check if the home page itself has the search form
    selects = wait_for_selects(driver, min_count=1, timeout=5)
    if selects:
        print(f"[*] Search form found on home page ({len(selects)} selects).")
        return driver.current_url

    # Try clicking a "Project" nav link
    print("[*] No form on home page; looking for project search link ...")
    link = find_project_search_link(driver)
    if link:
        href = link.get_attribute("href") or ""
        print(f"    Clicking: '{link.text.strip()}' -> {href}")
        try:
            driver.execute_script("arguments[0].click();", link)
            time.sleep(3)
            if diagnose:
                save_html(driver, "diagnose_after_click.html")
            selects = wait_for_selects(driver, min_count=1, timeout=PAGE_WAIT)
            if selects:
                print(f"[*] Form found after navigation ({len(selects)} selects).")
                return driver.current_url
        except Exception as e:
            print(f"    Click failed: {e}")

    # Try known direct URLs
    candidates = [
        f"{BASE_URL}/viewAllProjects?language=en",
        f"{BASE_URL}/viewProjects",
        f"{BASE_URL}/searchProject",
        f"{BASE_URL}/projectViewDetails",
    ]
    for url in candidates:
        print(f"[*] Trying {url} ...")
        try:
            driver.get(url)
            time.sleep(3)
            if diagnose:
                slug = url.replace("https://", "").replace("/", "_").replace("?", "_").replace("=", "_")
                save_html(driver, f"diagnose_{slug}.html")
            selects = wait_for_selects(driver, min_count=1, timeout=PAGE_WAIT)
            if selects:
                print(f"[*] Form found at {url} ({len(selects)} selects).")
                return driver.current_url
        except Exception as e:
            print(f"    Error: {e}")

    return None


# ── dropdown detection ────────────────────────────────────────────────────────

def find_select_by_options(driver, hints):
    """Find a <select> whose options contain any hint string."""
    selects = driver.find_elements(By.TAG_NAME, "select")
    for sel_el in selects:
        opts = get_options(driver, sel_el)
        for val, text in opts:
            if any(h in text.lower() for h in hints) and val:
                return sel_el, opts
    return None, []


def select_by_hint(select_el, options, hints):
    """Select first matching option; return (value, text) or (None, None)."""
    sel = Select(select_el)
    for val, text in options:
        for h in hints:
            if h in text.lower() and val:
                sel.select_by_value(val)
                return val, text
    return None, None


def dump_all_selects(driver):
    print("\n  All visible <select> options:")
    selects = driver.find_elements(By.TAG_NAME, "select")
    for i, sel_el in enumerate(selects):
        name = sel_el.get_attribute("name") or sel_el.get_attribute("id") or str(i)
        opts = get_options(driver, sel_el)
        print(f"    [{name}]")
        for v, t in opts:
            print(f"      {v!r:30s}  {t!r}")


# ── results extraction ────────────────────────────────────────────────────────

def extract_table(driver):
    tables = driver.find_elements(By.TAG_NAME, "table")
    if not tables:
        return []
    best = max(tables, key=lambda t: len(t.find_elements(By.TAG_NAME, "tr")))
    rows = best.find_elements(By.TAG_NAME, "tr")
    if len(rows) < 2:
        return []
    headers = [c.text.strip() for c in rows[0].find_elements(By.TAG_NAME, "th")]
    if not headers:
        headers = [c.text.strip() for c in rows[0].find_elements(By.TAG_NAME, "td")]
    records = []
    for row in rows[1:]:
        cells = row.find_elements(By.TAG_NAME, "td")
        if not cells:
            continue
        rec = {}
        for i, cell in enumerate(cells):
            key = headers[i] if i < len(headers) else f"col_{i}"
            rec[key] = cell.text.strip()
            links = cell.find_elements(By.TAG_NAME, "a")
            if links:
                rec[f"{key}_url"] = links[0].get_attribute("href") or ""
        records.append(rec)
    return records


def get_total_pages(driver):
    src = driver.page_source
    for pat in [
        r"of\s+([\d,]+)\s+(?:entries|records)",
        r'"recordsTotal"\s*:\s*(\d+)',
        r"Total\s*:?\s*([\d,]+)\s+(?:record|project)",
    ]:
        m = re.search(pat, src, re.IGNORECASE)
        if m:
            total = int(m.group(1).replace(",", ""))
            return max(1, -(-total // 10))
    nums = []
    for a in driver.find_elements(By.CSS_SELECTOR, ".pagination a, nav a"):
        t = a.text.strip()
        if t.isdigit():
            nums.append(int(t))
    return max(nums) if nums else 1


def click_next(driver, current_page):
    next_page = current_page + 1
    # Try page-number link
    try:
        links = driver.find_elements(By.LINK_TEXT, str(next_page))
        if links:
            driver.execute_script("arguments[0].click();", links[0])
            return True
    except Exception:
        pass
    # Try "Next" button variants
    for xpath in [
        "//a[normalize-space()='Next']",
        "//a[normalize-space()='>']",
        "//a[normalize-space()='»']",
        "//li[contains(@class,'next')]/a",
    ]:
        try:
            btn = driver.find_element(By.XPATH, xpath)
            if btn.is_enabled():
                driver.execute_script("arguments[0].click();", btn)
                return True
        except Exception:
            pass
    return False


def find_submit_button(driver):
    for sel in [
        "input[type='submit']", "button[type='submit']",
        "#searchBtn", "#submitBtn", "button.btn-primary",
        "button.btn-search", ".search-btn",
    ]:
        try:
            return driver.find_element(By.CSS_SELECTOR, sel)
        except Exception:
            pass
    try:
        btns = driver.find_elements(
            By.XPATH,
            "//button[contains(translate(.,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'search')"
            " or contains(translate(.,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'submit')]"
        )
        if btns:
            return btns[0]
    except Exception:
        pass
    return None


# ── per-district scrape ───────────────────────────────────────────────────────

def scrape_district(driver, form_url, district_val, district_name,
                    kreta_hints, diagnose=False):
    all_records = []
    page = 1

    while True:
        # Re-load the form page for each page to stay clean
        if page == 1:
            driver.get(form_url)
            time.sleep(3)
            selects = wait_for_selects(driver, min_count=1, timeout=PAGE_WAIT)
            if not selects:
                print(f"  [!] Form disappeared for {district_name}. Stopping.")
                break

            # Set district
            d_sel, d_opts = find_select_by_options(driver, DISTRICT_HINTS)
            if not d_sel:
                print(f"  [!] Lost district dropdown.")
                break
            sel = Select(d_sel)
            sel.select_by_value(district_val)
            print(f"  [*] District set: {district_name}")
            time.sleep(1)

            # Set kreta if available
            k_sel, k_opts = find_select_by_options(driver, kreta_hints)
            if k_sel:
                kv, kt = select_by_hint(k_sel, k_opts, kreta_hints)
                if kv:
                    print(f"  [*] Kreta filter set: {kt!r}")

            # Submit
            btn = find_submit_button(driver)
            if btn:
                driver.execute_script("arguments[0].click();", btn)
                print(f"  [*] Search submitted.")
                time.sleep(4)
            else:
                print(f"  [!] No submit button found; trying with current page content.")

        print(f"  [*] {district_name}  |  Page {page} ...")
        if diagnose:
            save_html(driver, f"diagnose_{district_name.replace(' ', '_')}_p{page}.html")

        # Wait for table
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table tr"))
            )
        except TimeoutException:
            print(f"  [!] Table not found on page {page}.")
            break

        records = extract_table(driver)
        if not records:
            print(f"  [!] No rows parsed on page {page}.")
            break

        for rec in records:
            rec["_district"] = district_name
            rec["_page"] = page
        all_records.extend(records)
        print(f"      -> {len(records)} rows  (total: {len(all_records)})")

        total_pages = get_total_pages(driver)
        if page >= total_pages:
            break
        if not click_next(driver, page):
            print(f"  [!] Cannot go to page {page + 1}. Stopping.")
            break
        page += 1
        time.sleep(2)

    return all_records


# ── main ─────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--show-browser", action="store_true",
                    help="Run with visible browser window")
    ap.add_argument("--diagnose", action="store_true",
                    help="Save HTML dumps of every page for debugging")
    args = ap.parse_args()

    driver = make_driver(headless=not args.show_browser)
    all_records = []

    try:
        # Step 1: Navigate to the form
        form_url = navigate_to_search_form(driver, diagnose=args.diagnose)
        if not form_url:
            print("\n[ERROR] Could not find the project search form on any page.")
            print("  Run with --show-browser and --diagnose to inspect what loads.")
            sys.exit(1)

        # Step 2: Discover district dropdown
        selects = wait_for_selects(driver, min_count=1, timeout=PAGE_WAIT)
        print(f"\n[*] {len(selects)} select(s) found on the search form page.")

        d_sel, d_opts = find_select_by_options(driver, DISTRICT_HINTS)
        if not d_sel:
            print("[!] Could not find district dropdown.")
            dump_all_selects(driver)
            if args.diagnose:
                save_html(driver, "diagnose_no_district.html")
            sys.exit(1)

        # Collect unique target districts
        seen, targets = set(), []
        for val, text in d_opts:
            for h in DISTRICT_HINTS:
                if h in text.lower() and val and val not in seen:
                    seen.add(val)
                    targets.append((val, text))

        print(f"[*] Target districts: {[t[1] for t in targets]}")

        # Step 3: Scrape each district
        for dist_val, dist_name in targets:
            print(f"\n[>] Scraping: {dist_name}")
            records = scrape_district(
                driver, form_url, dist_val, dist_name,
                KRETA_HINTS, diagnose=args.diagnose
            )
            all_records.extend(records)

    finally:
        driver.quit()

    if not all_records:
        print("\n[!] No records collected.")
        print("  Try: python3 scrape_rera_selenium.py --show-browser --diagnose")
        sys.exit(1)

    df = pd.DataFrame(all_records)
    out_path = "rera_properties.csv"
    df.to_csv(out_path, index=False, encoding="utf-8-sig")
    print(f"\n[+] {len(df)} records saved to {out_path}")
    print(df.head(3).to_string())


if __name__ == "__main__":
    main()
