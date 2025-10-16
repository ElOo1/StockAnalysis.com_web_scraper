from selenium.webdriver.common.by import By
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
def get_keywords_from_url(source, *keys):
    try:
        response = requests.get(source, headers={'User-Agent':'Mozilla/5.0'})
        response.raise_for_status()
        data = response.json()
    except (requests.RequestException, ValueError) as e:
        print(f"Error fetching or parsing JSON from URL: {e}")
        return None

    # Navigating the JSON Structure
    current_level = data
    for key in keys:
        # Returns the nested JSON for the key given
        current_level = current_level.get(key)
        if current_level is None:
            return None # Stop if key not found
    return current_level

# Access a nested value in a JSON file using a sequence of keys. Returns None if any key in the path is not found.
def get_keywords_from_file(filename, *keys):
    with open(filename, 'r') as f:
        # Load the json file content into a python object (dictionary or list)
        data = json.load(f)

    # Navigating the JSON Structure
    current_level = data
    for key in keys:
        # Returns the nested JSON for the key given
        current_level = current_level.get(key)
        if current_level is None:
            return None # Stop if key not found
    return current_level

# Format dynamic string. This can format strings with any amount of formats anywhere in the string.
def dynamic_string_format(string_template, counter=None, **kwargs):
    # Format string with a counter and additional kwargs
    format_kwargs = {}

    # Create a dictionary with counter and kwargs
    if counter is not None:
        format_kwargs['counter'] = counter
    else:
        0

    
    # Add all other kwargs
    format_kwargs.update(kwargs)

    return string_template.format(**format_kwargs)


# def dynamic_string_format(string_template, counter=None, **kwargs):
#     """
#     Format string where {counter} remains literal if counter=None.
#     Other placeholders format normally.
#     """
#     format_kwargs = kwargs.copy()
#     
#     if counter is not None:
#         format_kwargs['counter'] = counter
#         # Normal formatting
#         return string_template.format(**format_kwargs)
#     else:
#         # Counter not provided: format everything except {counter}
#         # Replace {counter} temporarily to avoid KeyError
#         temp_template = string_template.replace("{counter}", "TEMP_COUNTER_PLACEHOLDER")
#         formatted = temp_template.format(**format_kwargs)
#         # Restore literal {counter}
#         return formatted.replace("TEMP_COUNTER_PLACEHOLDER", "{counter}")


# Parse through Json file and extract data in pandas dataframe
def _extract_json_data_to_dataframe(base_url, columns_list, user_agent, browser):

    all_data = []
    counter = 1
    while True:
        # Notice we are passing the counter as a keyword argument to the dynamic_string_format function
        url = dynamic_string_format(base_url, counter=counter)
        response = requests.get(url, headers={user_agent: browser})

        json_list = response.json() # Assuming JSON response
        if not json_list: # Adjust based on API struture
            print("No Data")
            break

        for i in json_list:
            all_data.append([i.get(col, None) for col in columns_list])

        counter +=1
    return all_data



    


