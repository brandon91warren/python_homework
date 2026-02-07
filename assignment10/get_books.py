import json
import re
import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager


URL = "https://durhamcounty.bibliocommons.com/v2/search?query=learning%20spanish&searchType=smart"

FMT_WORDS = r"(Book|eBook|Audiobook|DVD|Music|Large Print|Graphic Novel|Magazine|Kit|Streaming Video|Streaming|Online)"
FMT_RE = re.compile(rf"\b{FMT_WORDS}\b", re.I)
YEAR_RE = re.compile(r"\b(19|20)\d{2}\b")


def clean_text(s):
    s = (s or "").replace("\u200b", "").replace("\u00a0", " ")
    return re.sub(r"\s+", " ", s).strip()


def strip_trailing_format(title):
    t = clean_text(title)
    t = re.sub(rf",\s*{FMT_WORDS}\b.*$", "", t, flags=re.I)
    return clean_text(t)


def load_with_retries(driver, url, tries=4):
    for i in range(tries):
        driver.get(url)
        time.sleep(2 + i * 2)
        if "502 Bad Gateway" not in driver.page_source:
            return True
    return False


def wait_for_results(driver, timeout=25):
    wait = WebDriverWait(driver, timeout)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "li.cp-search-result-item")))


def get_title(driver, li):
    title = ""
    a = None

    candidates = li.find_elements(By.CSS_SELECTOR, "h2.cp-title a")
    if candidates:
        a = candidates[0]
    else:
        candidates = li.find_elements(By.CSS_SELECTOR, "a.cp-title")
        if candidates:
            a = candidates[0]

    if a is None:
        return ""

    end = time.time() + 4.0
    while time.time() < end and not title:
        title = clean_text(driver.execute_script("return arguments[0].textContent;", a))
        if title:
            break
        title = clean_text(a.get_attribute("aria-label"))
        if title:
            break
        title = clean_text(a.get_attribute("title"))
        if title:
            break
        time.sleep(0.2)

    return strip_trailing_format(title)


def get_authors(li):
    author_els = li.find_elements(By.CSS_SELECTOR, "a.cp-author-link")
    names = [clean_text(a.text) for a in author_els if clean_text(a.text)]
    return "; ".join(names)


def pick_format_year(lines):
    lines = [clean_text(x) for x in lines if clean_text(x)]
    lines = [ln for ln in lines if not re.search(r"\(\s*\d+\s+rating", ln, re.I)]

    for ln in lines:
        if YEAR_RE.search(ln) and FMT_RE.search(ln):
            return ln
    for ln in lines:
        if YEAR_RE.search(ln):
            return ln
    for ln in lines:
        if FMT_RE.search(ln):
            return ln
    return ""


def get_format_year(li):
    info_els = li.find_elements(By.CSS_SELECTOR, "div.cp-search-result-item-info")
    if not info_els:
        return ""
    raw = info_els[0].get_attribute("innerText") or ""
    return pick_format_year(raw.splitlines())


def main():
    options = webdriver.ChromeOptions()
    options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    try:
        ok = load_with_retries(driver, URL)
        if not ok:
            raise RuntimeError("Site returned 502 after multiple retries. Try again later.")

        wait_for_results(driver, timeout=25)

        li_entries = driver.find_elements(By.CSS_SELECTOR, "li.cp-search-result-item")
        print(len(li_entries))

        results = []

        for i in range(len(li_entries)):
            li_entries = driver.find_elements(By.CSS_SELECTOR, "li.cp-search-result-item")
            li = li_entries[i]

            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", li)
            time.sleep(0.2)

            title = ""
            author = ""
            format_year = ""

            try:
                title = get_title(driver, li)
            except Exception:
                title = ""

            try:
                author = get_authors(li)
            except Exception:
                author = ""

            try:
                format_year = get_format_year(li)
            except Exception:
                format_year = ""

            results.append({"Title": title, "Author": author, "Format-Year": format_year})

        df = pd.DataFrame(results)
        print(df)

        df.to_csv("get_books.csv", index=False)

        with open("get_books.json", "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        print("\nWrote files: get_books.csv and get_books.json")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
