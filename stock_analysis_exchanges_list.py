from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests
import bs4
import sqlite3
import os

# Set up the webDriver (automatically downloads and configures ChromeDriver)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


login_url = "https://stockanalysis.com/login/"
data_url = "https://stockanalysis.com/list/exchanges"


try:
    # Navigate to the specific page on stockanalysis.com
    driver.get(login_url)

    # Login Credentials
    username_field = driver.find_element(By.ID, "email")
    password_field = driver.find_element(By.ID, "password")
    username_field.send_keys("GACM000001@gmail.com")
    password_field.send_keys("hizkem-danto1-dutguV")
    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    login_button.click()
    time.sleep(3)
    print("Login Successful")

except Exception as e:
    print(f"Error occured at login: {e}")


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

except Exception as e:
    print(f"Error occured navigation: {e}")



# stock_analysis_file_name = "stock_analysis_financial_data.db"

# stock_analysis_db_path = os.getcwd() + "/"

# stock_analysis_file = stock_analysis_db_path + stock_analysis_file_name

# connection = sqlite3.connect(stock_analysis_file)

# cursor = connection.cursor()

# cursor.execute("""
#     """)

# Create a session to persist cookies
session = requests.Session()

# URL of the login page and the target data page
data_url = "https://stockanalysis.com/list/exchanges"


# Send POST request to login

#response = session.get(data_url)

# Check if login was successful
# try:
#     if response.status_code == 200:
#         print("Login sucessful")
# except Exception as e:
#     print(f"Login Failed. Status code '{e}'")



