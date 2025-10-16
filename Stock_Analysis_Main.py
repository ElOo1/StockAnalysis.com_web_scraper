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
            print("No table on page.")
            return []

        complete_table_data = []

        # Extract table headers
        headers = data_processing._extract_table_headers(driver, table_selector)
        complete_table_data.append(headers)
        print("headrs appended")

        while True:
            wait = WebDriverWait(driver, 5)
            table = wait.until(EC.presence_of_element_located((By.XPATH, "//table")))
            # Wait for the table to be present
            # time.sleep(3) # Allow page to load after clicking

            rows = data_processing._extract_table_rows(driver, table_selector)

            complete_table_data.append(rows)

            element = driver.find_element(By.XPATH, next_button_selector)

            element.click()

            if not element.is_enabled():
                break

        return complete_table_data

    except Exception as e:
        print(f"Error occured navigation: {e}")
        return []
    finally:
        driver.quit()
