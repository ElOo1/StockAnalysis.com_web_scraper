# To erase the db database
import sqlite3
import os

stock_analysis_file_name = "stock_analysis_financial_data.db"

stock_analysis_db_path = os.getcwd() + "/"

stock_analysis_file = stock_analysis_db_path + stock_analysis_file_name

if os.path.exists(stock_analysis_file):
    
    connection = sqlite3.connect(stock_analysis_file)

    cursor = connection.cursor()

    cursor.execute("""
        DROP TABLE Stock_Analysis_Exchange_List
    """)
else:
    print(f"File '{stock_analysis_file}' does not exist.")
