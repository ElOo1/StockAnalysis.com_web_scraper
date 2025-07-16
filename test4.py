from sys import exception
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from datetime import date
import time
from Stock_Analysis_Main import *

# Set up the WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
data_url = "https://stockanalysis.com/list/otc-stocks/"
button_name = "button.controls-btn.xs\:pl-1.xs\:pr-1\.5.bp\:text-sm.sm\:pl-3.sm\:pr-1"
login_button_name = "//button[@type='submit']"
#button_name = "button[data-test='next-page']"  # Updated CSS selector for "Next" button

login_url = "https://stockanalysis.com/login/"
user_field = "email"
pass_field = "password"
user = "GACM000001@gmail.com"
password = "hizkem-danto1-dutguV"

# Initialize driver and log in
driver = web_navigation.initialize_driver()
login_sucess = web_navigation.login_to_website(driver, login_url, user_field, pass_field, user, password, login_button_name)

if not login_sucess:
    print("Login failed, exiting.")
    driver.quit()
    exit()

# Navigate to data page
driver.get(data_url)
time.sleep(3)  # Wait for page to load

table_data = []

for i in range(3):
    try:
        wait = WebDriverWait(driver, 5)
        table = wait.until(EC.presence_of_element_located((By.XPATH, "//table")))
        # Extract table rows
        rows = table.find_elements(By.XPATH, "//tbody/tr")
        print(len(rows))
        for row in rows:
            # Extract cells in each row
            cells = [cell.text.strip() for cell in row.find_elements(By.XPATH, ".//td")]
            cells.append(str(date.today()))
            table_data.append(cells)
        button = driver.find_element(By.CSS_SELECTOR, button_name)
        button.click()
        print("button found and clicked")
        # Wait for the table to be present
        # Wait for the table to be present
        wait = WebDriverWait(driver, 5)
        time.sleep(3)  # Wait for page to load
    except Exception as e:
        print("button not found")

print(table_data)
