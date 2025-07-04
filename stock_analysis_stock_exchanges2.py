from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from Stock_Analysis_Main import login_to_website, table_data_extract_from_html

# Set up the webDriver (automatically downloads and configures ChromeDriver)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

file_name = "stock_exchanges.csv"
login_url = "https://stockanalysis.com/login/"
data_url = "https://stockanalysis.com/list/exchanges"
file_path = "/Users/elmisomari/Desktop/Files/Projects/Webscraping/stock_exchanges.csv"

user_field = "email"
pass_field = "password"
user = "GACM000001@gmail.com"
password = "hizkem-danto1-dutguV"

login_to_website(login_url, user_field, pass_field, user, password)
table_data_extract_from_html(data_url, file_name )
