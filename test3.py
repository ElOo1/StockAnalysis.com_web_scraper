from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import date
import csv
import time
import os

# Set up the WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# URLs and file paths
file_name = "Over_The_Counter_Stocks.csv"
login_url = "https://stockanalysis.com/login/"
data_url = "https://stockanalysis.com/list/otc-stocks/"
file_path = f"/Users/elmisomari/Desktop/Files/Projects/Webscraping/{file_name}"

# Login credentials (uncomment and use if login is required)
user_field = "email"
pass_field = "password"
user = "GACM000001@gmail.com"
password = "hizkem-danto1-dutguV"

# Selectors
next_table_button = ".controls-btn"  # CSS selector for the Next button

def login_to_website(driver, login_url, user_field, pass_field, user, password):
    try:
        driver.get(login_url)
        wait = WebDriverWait(driver, 10)
        # Enter username
        username_input = wait.until(EC.presence_of_element_located((By.NAME, user_field)))
        username_input.send_keys(user)
        # Enter password
        password_input = driver.find_element(By.NAME, pass_field)
        password_input.send_keys(password)
        # Submit login form
        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()
        time.sleep(2)  # Wait for login to complete
        print("Login successful")
    except Exception as e:
        print(f"Login failed: {e}")
        driver.save_screenshot("login_error.png")
        driver.quit()
        exit()

# Uncomment the following line if login is required
# login_to_website(driver, login_url, user_field, pass_field, user, password)

# Navigate to data page
driver.get(data_url)
time.sleep(3)  # Wait for page to load

# Print page title to confirm navigation
try:
    page_title = driver.find_element(By.TAG_NAME, "h1").text
    print(f"Navigated to page: {page_title}")
except Exception as e:
    print(f"Error finding page title: {e}")

# Wait for table to load
wait = WebDriverWait(driver, 10)  # Increased timeout
try:
    table = wait.until(EC.visibility_of_element_located((By.XPATH, "//table")))
    print("Table found")
except Exception as e:
    print(f"Error finding table: {e}")
    driver.save_screenshot("table_error.png")
    driver.quit()
    exit()

# Extract table rows
table_data = []
rows = table.find_elements(By.XPATH, ".//tbody/tr")
for row in rows:
    cells = [cell.text.strip() for cell in row.find_elements(By.XPATH, ".//td")]
    if cells and cells not in table_data:  # Avoid duplicates and empty rows
        cells.append(str(date.today()))
        table_data.append(cells)

# Save initial table data to CSV
try:
    with open(file_path, "w", newline="", encoding="utf-8") as new_file:
        writer = csv.writer(new_file)
        writer.writerows(table_data)
    print(f"Initial data saved to {file_path} with {len(table_data)} rows")
except Exception as e:
    print(f"Error saving initial data to CSV: {e}")

# Handle pagination
try:
    while True:
        try:
            # Wait for the Next button to be clickable
            button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, next_table_button)))
            if button.get_attribute("disabled") or not button.is_enabled():
                print("No more pages to load")
                break
            button.click()
            print("Clicked Next button")
            time.sleep(2)  # Wait for new content to load
            # Re-extract table rows
            rows = table.find_elements(By.XPATH, ".//tbody/tr")
            for row in rows:
                cells = [cell.text.strip() for cell in row.find_elements(By.XPATH, ".//td")]
                if cells and cells not in table_data:
                    cells.append(str(date.today()))
                    table_data.append(cells)
        except Exception as e:
            print(f"Error during pagination: {e}")
            driver.save_screenshot("pagination_error.png")
            # Save page source for debugging
            with open("page_source.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            break
except Exception as e:
    print(f"Error finding pagination button: {e}")
    driver.save_screenshot("pagination_error.png")
    with open("page_source.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)

# Save final table data to CSV
try:
    with open(file_path, "w", newline="", encoding="utf-8") as new_file:
        writer = csv.writer(new_file)
        writer.writerows(table_data)
    print(f"Final data saved to {file_path} with {len(table_data)} rows")
except Exception as e:
    print(f"Error saving final data to CSV: {e}")

# Print extracted data for debugging
print(f"Extracted data: {table_data}")

# Clean up
driver.quit()
