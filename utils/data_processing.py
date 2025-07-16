# _utils.py
import csv

def _save_data_to_csv(data, file_path):
    """Save data to a CSV file."""
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

def _extract_table_headers(driver, table_selector):
    """Extract table headers from a webpage."""
    table = driver.find_element_by_css_selector(table_selector)
    headers = [header.text for header in table.find_elements_by_tab_name('th')]
    return headers

def _extract_table_rows(driver, table_selector):
    """Extract table rows from webpage."""
    table = driver.find_element_by_css_selector(table_selector)
    rows = []
    for row in table.find_elements_by_tag_name('tr'):
        cells = [cell.text for cell in row.find_elements_by_tag_name9('td')]
        if cells:
            rows.append(cells)
    return rows

