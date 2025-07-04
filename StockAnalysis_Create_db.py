import sqlite3
import os

stock_analysis_file_name = "stock_analysis_financial_data.db"

# Create the db file 
try:
    with open(stock_analysis_file_name, "x") as file:
        # File created successfully
        print("File created successfully")
except FileExistsError:
    print("File already exists")


stock_analysis_db_path = os.getcwd() + "/"

stock_analysis_file = stock_analysis_db_path + stock_analysis_file_name

connection = sqlite3.connect(stock_analysis_file)

cursor = connection.cursor()


cursor.execute("""
    CREATE TABLE IF NOT EXISTS Stock_Analysis_Exchange_List (
    id INTEGER PRIMARY KEY,
    exchange TEXT,
    country TEXT,
    exchange_code TEXT,
    currency TEXT,
    number_of_listed_stocks TEXT,
    upload_date TEXT
    )
    """)


