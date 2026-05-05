"""
RERA Karnataka Property Scraper — Selenium version
Use this if the requests-based scraper (scrape_rera_properties.py) fails
because the site renders results via JavaScript.

Requirements:
    pip install selenium webdriver-manager pandas
    # Chrome or Firefox must be installed

Run:
    python3 scrape_rera_selenium.py
Output:
    rera_properties.csv
"""

import time
import re
import sys
import pandas as pd

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import Select, WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options as ChromeOptions
    from selenium.webdriver.firefox.options import Options as FirefoxOptions
except ImportError:
    print("[ERROR] selenium not installed. Run: pip install selenium webdriver-manager")
    sys.exit(1)

SEARCH_URL = "https://rera.karnataka.gov.in/projectViewDetails"

TARGET_DISTRICTS = [
    "Bengaluru Urban",
    "Bangalore Urban",
    "South Bengaluru",
    "Bangalore South",
    "BBMP South",
]

KRETA_HINTS = ["kreta", "buyer", "purchaser", "complainant"]


def make_driver(headless=True):
    """Try Chrome first, then Firefox."""
    # Chrome
    try:
        opts = ChromeOptions()
        if headless:
            opts.add_argument("--headless=new")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--window-size=1400,900")
        opts.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36"
        )
        driver = webdriver.Chrome(options=opts)
        print("[*] Using Chrome WebDriver")
        return driver
    except Exception as ce:
        print(f"[!] Chrome failed ({ce}), trying Firefox ...")

    # Firefox
    try:
        opts = FirefoxOptions()
        if headless:
            opts.add_argument("--headless")
        driver = webdriver.Firefox(options=opts)
        print("[*] Using Firefox WebDriver")
        return driver
    except Exception as fe:
        print(f"[ERROR] Firefox also failed: {fe}")
        print("Install Chrome or Firefox and the matching WebDriver.")
        sys.exit(1)


def wait_for_table(driver, timeout=20):
    """Wait until at least one <tr> appears inside any <table>."""
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table tr"))
        )
        return True
    except Exception:
        return False


def get_select_options(driver, select_elem):
    """Return list of (value, text) for a <select> element."""
    sel = Select(select_elem)
    return [(o.get_attribute("value"), o.text.strip()) for o in sel.options]


def find_target_select(driver, hints):
    """Find a <select> whose options include any of the hint strings."""
    selects = driver.find_elements(By.TAG_NAME, "select")
    for sel_el in selects:
        options = get_select_options(driver, sel_el)
        for val, text in options:
            for hint in hints:
                if hint.lower() in text.lower() and val:
                    return sel_el, options
    return None, []


def select_option_by_hint(driver, select_el, options, hints):
    """Select first option whose text contains any hint."""
    sel = Select(select_el)
    for val, text in options:
        for hint in hints:
            if hint.lower() in text.lower() and val:
                sel.select_by_value(val)
                print(f"    Selected: {text!r} (value={val!r})")
                return val, text
    return None, None


def extract_table_data(driver):
    """Extract all rows from the (first/largest) table on the page."""
    tables = driver.find_elements(By.TAG_NAME, "table")
    if not tables:
        return []

    # Pick the table with the most rows
    best = max(tables, key=lambda t: len(t.find_elements(By.TAG_NAME, "tr")))
    rows = best.find_elements(By.TAG_NAME, "tr")
    if not rows:
        return []

    # Headers
    header_cells = rows[0].find_elements(By.TAG_NAME, "th")
    if not header_cells:
        header_cells = rows[0].find_elements(By.TAG_NAME, "td")
    headers = [c.text.strip() for c in header_cells]

    records = []
    for row in rows[1:]:
        cells = row.find_elements(By.TAG_NAME, "td")
        if not cells:
            continue
        rec = {}
        for i, cell in enumerate(cells):
            key = headers[i] if i < len(headers) else f"col_{i}"
            rec[key] = cell.text.strip()
            # Capture hyperlinks
            links = cell.find_elements(By.TAG_NAME, "a")
            if links:
                rec[f"{key}_url"] = links[0].get_attribute("href") or ""
        records.append(rec)
    return records


def get_total_pages(driver):
    """Detect number of pages from pagination or record count text."""
    src = driver.page_source
    # DataTables: recordsTotal
    m = re.search(r'"recordsTotal"\s*:\s*(\d+)', src)
    if m:
        total = int(m.group(1))
        return max(1, -(-total // 10))

    # "Showing X to Y of Z entries"
    m = re.search(r"of\s+([\d,]+)\s+(?:entries|records)", src, re.IGNORECASE)
    if m:
        total = int(m.group(1).replace(",", ""))
        return max(1, -(-total // 10))

    # Pagination links
    try:
        page_links = driver.find_elements(By.CSS_SELECTOR, ".pagination a, nav a")
        nums = []
        for a in page_links:
            t = a.text.strip()
            if t.isdigit():
                nums.append(int(t))
        if nums:
            return max(nums)
    except Exception:
        pass

    return 1


def click_next_page(driver, current_page):
    """
    Click the next page button. Returns True if successful.
    Tries common pagination patterns.
    """
    next_page = current_page + 1

    # Try link with exact page number text
    try:
        links = driver.find_elements(By.LINK_TEXT, str(next_page))
        if links:
            driver.execute_script("arguments[0].click();", links[0])
            return True
    except Exception:
        pass

    # Try "Next" button
    for selector in ["a.next", "a[aria-label='Next']", "#next", ".next a", "a:contains('Next')"]:
        try:
            btn = driver.find_element(By.CSS_SELECTOR, selector)
            if btn.is_enabled():
                driver.execute_script("arguments[0].click();", btn)
                return True
        except Exception:
            pass

    # Try button with text "Next" or ">"
    try:
        btns = driver.find_elements(By.XPATH, "//a[normalize-space()='Next' or normalize-space()='>']")
        if btns:
            driver.execute_script("arguments[0].click();", btns[0])
            return True
    except Exception:
        pass

    return False


def scrape_district(driver, district_name):
    """Scrape all pages for the currently-selected district."""
    all_records = []
    page = 1

    while True:
        print(f"  [*] {district_name}  |  Page {page} ...")
        time.sleep(2)

        if not wait_for_table(driver, timeout=15):
            print(f"  [!] Table not found on page {page}.")
            break

        records = extract_table_data(driver)
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

        if not click_next_page(driver, page):
            print(f"  [!] Cannot navigate to page {page + 1}. Stopping.")
            break

        page += 1

    return all_records


def find_submit_button(driver):
    """Return the search/submit button element."""
    for sel in [
        "input[type='submit']",
        "button[type='submit']",
        "button.search-btn",
        "button.btn-primary",
        "#searchBtn",
        "#submitBtn",
    ]:
        try:
            btn = driver.find_element(By.CSS_SELECTOR, sel)
            return btn
        except Exception:
            pass

    # Fallback: any button with text search/submit/go
    try:
        btns = driver.find_elements(
            By.XPATH,
            "//button[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'search')"
            " or contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'submit')"
            " or contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'go')]"
        )
        if btns:
            return btns[0]
    except Exception:
        pass

    return None


def main(headless=True):
    driver = make_driver(headless=headless)
    all_records = []

    try:
        print(f"[*] Opening {SEARCH_URL}")
        driver.get(SEARCH_URL)
        time.sleep(3)

        print("[*] Discovering form selects ...")
        selects = driver.find_elements(By.TAG_NAME, "select")
        print(f"    Found {len(selects)} <select> element(s)")

        for i, sel_el in enumerate(selects):
            opts = get_select_options(driver, sel_el)
            name = sel_el.get_attribute("name") or sel_el.get_attribute("id") or f"select_{i}"
            print(f"    [{name}]  {len(opts)} options: {[t for _, t in opts[:5]]} ...")

        # Find district select
        district_select, district_options = find_target_select(driver, TARGET_DISTRICTS)
        if not district_select:
            print("[!] Could not find district dropdown. Dumping all options:")
            for i, sel_el in enumerate(selects):
                opts = get_select_options(driver, sel_el)
                name = sel_el.get_attribute("name") or str(i)
                for v, t in opts:
                    print(f"    [{name}] {v!r} -> {t!r}")
            sys.exit(1)

        # Find kreta select
        kreta_select = None
        kreta_options = []
        for sel_el in selects:
            if sel_el == district_select:
                continue
            opts = get_select_options(driver, sel_el)
            for _, text in opts:
                if any(h in text.lower() for h in KRETA_HINTS):
                    kreta_select = sel_el
                    kreta_options = opts
                    break

        if kreta_select:
            print(f"[*] Kreta filter dropdown found.")
        else:
            print("[!] No kreta filter found; scraping without it.")

        # Collect distinct district targets (value + display text)
        seen_vals = set()
        targets = []
        for val, text in district_options:
            for hint in TARGET_DISTRICTS:
                if hint.lower() in text.lower() and val and val not in seen_vals:
                    seen_vals.add(val)
                    targets.append((val, text))

        print(f"[*] Will scrape {len(targets)} district(s): {[t for _, t in targets]}")

        for dist_val, dist_name in targets:
            print(f"\n[>] Scraping: {dist_name}")
            driver.get(SEARCH_URL)
            time.sleep(2)

            # Re-find elements after navigation
            selects = driver.find_elements(By.TAG_NAME, "select")
            d_sel, d_opts = find_target_select(driver, TARGET_DISTRICTS)
            if not d_sel:
                print(f"  [!] Lost district dropdown. Skipping {dist_name}.")
                continue

            # Select district
            sel_obj = Select(d_sel)
            try:
                sel_obj.select_by_value(dist_val)
                print(f"  [*] District set to: {dist_name}")
                time.sleep(1)
            except Exception as e:
                print(f"  [!] Could not select district value {dist_val!r}: {e}")
                continue

            # Select kreta if available
            if kreta_select:
                # Re-find the kreta select after navigation
                for sel_el in driver.find_elements(By.TAG_NAME, "select"):
                    opts = get_select_options(driver, sel_el)
                    for v, t in opts:
                        if any(h in t.lower() for h in KRETA_HINTS):
                            ksel = Select(sel_el)
                            ksel.select_by_value(v)
                            print(f"  [*] Kreta filter set: {t!r}")
                            time.sleep(0.5)
                            break

            # Click search
            submit_btn = find_submit_button(driver)
            if submit_btn:
                driver.execute_script("arguments[0].click();", submit_btn)
                print(f"  [*] Search submitted.")
                time.sleep(3)
            else:
                print(f"  [!] Submit button not found; results may already be loaded.")

            records = scrape_district(driver, dist_name)
            all_records.extend(records)

    finally:
        driver.quit()

    if not all_records:
        print("\n[!] No records collected.")
        sys.exit(1)

    df = pd.DataFrame(all_records)
    out_path = "rera_properties.csv"
    df.to_csv(out_path, index=False, encoding="utf-8-sig")
    print(f"\n[+] Done! {len(df)} total records saved to {out_path}")
    print(df.head(3).to_string())


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--show-browser", action="store_true",
                    help="Run with visible browser window (not headless)")
    args = ap.parse_args()
    main(headless=not args.show_browser)
