from selenium.webdriver.common.by import By
import pandas as pd
import requests
import json
# _utils.py
import csv

def _save_data_to_csv(data, file_path):
    """Save data to a CSV file."""
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

def _extract_table_headers(driver, table_selector):
    """Extract table headers from a webpage."""
    table = driver.find_element(By.CSS_SELECTOR, table_selector)
    headers = [header.text for header in table.find_elements(By.TAG_NAME, 'th')]
    return headers

def _extract_table_rows(driver, table_selector):
    """Extract table rows from webpage."""
    table = driver.find_element(By.CSS_SELECTOR, table_selector)
    rows = []
    for row in table.find_elements(By.TAG_NAME, 'tr'):
        cells = [cell.text for cell in row.find_elements(By.TAG_NAME, 'td')]
        if cells:
            rows.append(cells)
    return rows

# Access a nested value in a JSON file using a sequence of keys. Returns None if any key in the path is not found.
def get_url_source_data(source):
    try:
        response = requests.get(source, headers={'User-Agent':'Mozilla/5.0'})
        response.raise_for_status()
        data = response.json()
        return data
    except (requests.RequestException, ValueError) as e:
        print(f"Error fetching or parsing JSON from URL: {e}")
        return None

# Access a nested value in a JSON file using a sequence of keys. Returns None if any key in the path is not found.
def get_file_source_data(filename):
    with open(filename, 'r') as f:
        # Load the json file content into a python object (dictionary or list)
        data = json.load(f)
    return data

# Format dynamic string. This can format strings with any amount of formats anywhere in the string.
# def dynamic_string_format(string_template, counter=None, **kwargs):
#     # Format string with a counter and additional kwargs
#     format_kwargs = {}

#     # Create a dictionary with counter and kwargs
#     if counter is not None:
#         format_kwargs['counter'] = counter
#     else:
#         0

#     
#     # Add all other kwargs
#     format_kwargs.update(kwargs)

#     return string_template.format(**format_kwargs)


def dynamic_string_format(string_template, counter=None, **kwargs):
    """
    Format string where {counter} remains literal if counter=None.
    Other placeholders format normally.
    """
    format_kwargs = kwargs.copy()
    
    if counter is not None:
        format_kwargs['counter'] = counter
        # Normal formatting
        return string_template.format(**format_kwargs)
    else:
        # Counter not provided: format everything except {counter}
        # Replace {counter} temporarily to avoid KeyError
        temp_template = string_template.replace("{counter}", "TEMP_COUNTER_PLACEHOLDER")
        formatted = temp_template.format(**format_kwargs)
        # Restore literal {counter}
        return formatted.replace("TEMP_COUNTER_PLACEHOLDER", "{counter}")

def add_columns_to_Dataframe(columns_list):
    df = pd.DataFrame()
    for i in columns_list:
        df.add(i)
    return df

# Access a nested value in a JSON file using a sequence of keys. Returns None if any key in the path is not found.
def navigate_to_desired_level_data(source, *keys):
    # Navigating the JSON Structure
    for key in keys:
        # Returns the nested JSON for the key given
        source = source.get(key)
        if source is None:
            return None # Stop if key not found
    return source

# Parse through Json file and extract data in pandas dataframe
def _extract_json_data_to_dataframe(json, columns_list):

    all_data = []
    counter = 1

    if not isinstance(json, list):
        # Adjust based on API struture
        print("No Data")

        for i in json:
            all_data.append([i[1].get(col, None) for col in columns_list])

        counter +=1
    return all_data



