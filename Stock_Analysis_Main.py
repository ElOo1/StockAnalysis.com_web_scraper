from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import date
from utils import data_processing
from utils import web_navigation
import time


def scrape_table_website(driver, url, table_selector, next_button_selector):
    "Function to scrape a table and save to csv"
    try:
        driver.get(url)
        time.sleep(3)

        # Verify the page loaded by checking element in page
        page_title = driver.find_element(By.TAG_NAME, "h1").text
        print(f"Naigated to page: {page_title}")

        # Wait for the table to be present
        wait = WebDriverWait(driver, 5)
        table = wait.until(EC.presence_of_element_located((By.XPATH, "//table")))
        if table:
            print("Table exists in page.")
        else:
            return print("No table on page.")

        complete_table_data = []
        # Extract table headers
        headers = data_processing._extract_table_headers(driver, table_selector)
        complete_table_data.append(headers)

        while True:
            # Wait for the table to be present
            rows = data_processing._extract_table_rows(driver, table_selector)
            web_navigation.button_click(driver, next_button_selector)
            complete_table_data.append(rows)
            if web_navigation.is_button_disabled(driver, url, next_button_selector):
                break

        return complete_table_data

    except Exception as e:
        return print(f"Error occured navigation: {e}")
    finally:
        driver.quit()
