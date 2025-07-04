from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from Stock_Analysis_Main import *
import time

# Set up the webDriver (automatically downloads and configures ChromeDriver)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

file_name = "Over_The_Counter_Stocks.csv"
login_url = "https://stockanalysis.com/login/"
data_url = "https://stockanalysis.com/list/otc-stocks/"
file_path = "/Users/elmisomari/Desktop/Files/Projects/Webscraping/" + file_name
button_name = "button.controls-btn.xs\:pl-1.xs\:pr-1\.5.bp\:text-sm.sm\:pl-3.sm\:pr-1"

next_table_button = ".controls-btn"
next_table_button2 = "//button[contains(@class, 'controls-btn')]"


user_field = "email"
pass_field = "password"
user = "GACM000001@gmail.com"
password = "hizkem-danto1-dutguV"


#login_to_website(login_url, user_field, pass_field, user, password)
#button_download_data(data_url, "Over_The_Counter_Stocks.csv", file_path)
#iterable_table_data_extract_from_html(data_url, file_name, next_table_button)
is_button_disabled(data_url, button_name)
