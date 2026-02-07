import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager


START_URL = "https://owasp.org/www-project-top-ten/"
TOP10_2025_URL = "https://owasp.org/Top10/2025/"


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
        driver.get(START_URL)

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        driver.get(TOP10_2025_URL)

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//ol[.//a[contains(normalize-space(.), 'A01:')]]"))
        )

        xpath_links = "//ol[.//a[contains(normalize-space(.), 'A01:')]]/li/a"
        links = driver.find_elements(By.XPATH, xpath_links)

        results = []
        for a in links[:10]:
            title = (a.text or "").strip()
            href = a.get_attribute("href")
            results.append({"Title": title, "Link": href})

        print(results)

        df = pd.DataFrame(results)
        df.to_csv("owasp_top_10.csv", index=False)
        print("\nWrote file: owasp_top_10.csv")

        time.sleep(0.5)

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
