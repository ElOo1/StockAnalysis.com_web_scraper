from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import date
import csv
import time
import os

# Set up the webDriver (automatically downloads and configures ChromeDriver)
def initialize_driver():
    return  webdriver.Chrome(service=Service(ChromeDriverManager().install()))

def login_to_website(driver, login_url: str, username_field: str, password_field: str, username: str, password: str, login_button: str):
    """Log in to the website and verify login success."""
    try:
        driver.get(login_url)
        time.sleep(1) # Allow page to load

        #Enter credentials
        username_field_elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, username_field)))
        password_field_elem = driver.find_element(By.ID, password_field)
        username_field_elem.send_keys(username)
        password_field_elem.send_keys(password)

        # Click login button
        login_button_elem = driver.find_element(By.XPATH, login_button)
        login_button_elem.click()

        # Verify login success by checking for a post-login element
        WebDriverWait(driver, 10).until((EC.presence_of_element_located(By.XPATH, "//a[contains(text(), 'Log out')] | //div[contains(@class, 'user-profile')]")))
        print("Login Successful")
        return True
    except Exception as e:
        print(f"Error during login: {e}")
        return False

def login_to_website(login_url: str, username_field: str, password_field: str, username: str, password: str):
    try:
        # Navigate to the specific page on stockanalysis.com
        driver.get(login_url)

        # Login Credentials
        usernamefield = driver.find_element(By.ID, username_field)
        passwordfield = driver.find_element(By.ID, password_field)
        usernamefield.send_keys(username)
        passwordfield.send_keys(password)
        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()
        time.sleep(3)
        return print("Login Successful")

    except Exception as e:
        return print(f"Error occured at login: {e}")
    # finally:
    #     driver.quit()


def table_data_extract_from_html(data_url: str, csv_file_name: str):
    # Exchanges Lists
    try:
        driver.get(data_url)
        time.sleep(3)

        # Verify the page loaded by checking element in page
        page_title = driver.find_element(By.TAG_NAME, "h1").text
        print(f"Naigated to page: {page_title}")

        # Wait for the table to be present
        wait = WebDriverWait(driver, 5)
        table = wait.until(EC.presence_of_element_located((By.XPATH, "//table")))

        # Extract table headers
        headers = [header.text.strip() for header in table.find_elements(By.XPATH, ".//thead//th")]
        headers.append("Date of Collection")

        # Extract table rows
        rows = table.find_elements(By.XPATH, ".//tbody/tr")
        table_data = []
        table_data.append(headers)
        for row in rows:
            # Extract cells in each row
            cells = [cell.text.strip() for cell in row.find_elements(By.XPATH, ".//td")]
            cells.append(str(date.today()))
            table_data.append(cells)

        # Save data to csv
        with open(csv_file_name, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            # Write data rows
            writer.writerows(table_data)

        return print(f"Data scraped and saved successfully to {csv_file_name} with {len(table_data)} rows.")

    except Exception as e:
        return print(f"Error occured navigation: {e}")

# Check if button is enabeled and clickable
def is_button_disabled(data_url: str, button_name: str):

    # Desired Url
    driver.get(data_url)
    time.sleep(3)

    try:
        # Wait for the button to be present
        wait = WebDriverWait(driver, 5)
        button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, button_name)))

        # Method 1: Check is_enabled()
        is_enabled = button.is_enabled()

        # Method 2: Check for disabled attribute
        disabled_attr = button.get_attribute("disabled")

        # Method 3: Check for disabled class (if applicable)
        class_list = button.get_attribute("class")
        has_disabled_class = "disabled" in class_list or "opacity"
        return not is_enabled or disabled_attr is not None or has_disabled_class
    except Exception as e:
        print(f"Error checking button state: {str(e)}")
    


def button_download_data (data_url: str, csv_file_name: str, csv_file_path: str):
    if os.path.exists(csv_file_path):
        print("File already exists")
        answer  = input("Would you like to continue by appending latest version Y/N: ")
        if answer == "N":
            return print("No new file appended")
        else:
            # Exchanges Lists
            try:
                # Get list of download files before desired file download

                driver.get(data_url)
                time.sleep(3)

                # Find and click the download button
                download_button = driver.find_element(By.XPATH,"//button[text()='Download to CSV']")
                download_button.click()

                # Wait for the CSV file to be present

                # Save data to csv
                return print(f"CSV data downloaded and saved successfully to {csv_file_name}  .")


            except Exception as e:
                return print(f"Error occured navigation: {e}")


def iterable_table_data_extract_from_html(data_url: str, csv_file_name: str, button_class_name: str):
    try:
        driver.get(data_url)
        time.sleep(3)

        # Verify the page loaded by checking element in page
        page_title = driver.find_element(By.TAG_NAME, "h1").text
        print(f"Naigated to page: {page_title}")

        # Wait for the table to be present
        wait = WebDriverWait(driver, 5)
        table = wait.until(EC.presence_of_element_located((By.XPATH, "//table")))
        # Extract table headers
        headers = [header.text.strip() for header in table.find_elements(By.XPATH, ".//thead//th")]
        headers.append("Date of Collection")
        table_data = [headers]


        while True:
            try:
                

                # Wait for the table to be present
                wait = WebDriverWait(driver, 5)
                table = wait.until(EC.presence_of_element_located((By.XPATH, "//table")))
                # Extract table rows
                rows = table.find_elements(By.XPATH, ".//tbody/tr")

                table_data = []
                table_data.append(headers)
                for row in rows:
                    # Extract cells in each row
                    cells = [cell.text.strip() for cell in row.find_elements(By.XPATH, ".//td")]
                    if cells not in table_data: # Avoid duplicates
                        cells.append(str(date.today()))
                        table_data.append(cells)

                # Wait for button to be clickable
                button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, button_class_name)))

                # Check if button is disabled
                if button.get_attribute("disabled") or not button.is_enabled():
                    print("Button is disabled, stopping clicks.")
                    break

                # Click the button to load more data
                button.click()
                # Brief pause for content to load
                time.sleep(1)  

            except Exception as e:
                print(f"Error during button click or data extraction: {e}")
                break

    except Exception as e:
        return print(f"Error occured navigation: {e}")
    finally:
        driver.quit()
