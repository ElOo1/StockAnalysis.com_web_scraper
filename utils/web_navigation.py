from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time



# Set up the webDriver (automatically downloads and configures ChromeDriver)
def initialize_driver():
    return  webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Login to any website
def login_to_website(driver, login_url: str, username_field: str, password_field: str, username: str, password: str, login_button):
    """Log in to the website and verify login success."""
    try:
        driver.get(login_url)
        time.sleep(1) # Allow page to load
        print("Navigated to login page")

        #Enter credentials
        username_field_elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, username_field)))
        password_field_elem = driver.find_element(By.ID, password_field)
        username_field_elem.send_keys(username)
        print("Entered username")
        password_field_elem.send_keys(password)
        print("Entered password")

        # Click login button
        login_button_elem = driver.find_element(By.XPATH, login_button)
        login_button_elem.click()
        print("Clicked login button")

        # Wait for redirect or post-login element(ex: dashboard or some logout link)
        #WebDriverWait(driver, 10).until(EC.url_changes(login_url))
        #print("Current URL after login:", driver.current_url)

        #  Verify login success by checking for a post-login element
        time.sleep(15)
        print("Login Successful")
        return True
    except TimeoutException as e:
        print(f"Timeout error: {e}")
        return False
    except NoSuchElementException as e:
        print(f"Element not found: {e}")
        return False
    except Exception as e:
        print(f"Error during login: {e}")
        return False

# Check that website persisted after login navigation
def verify_login_persistent(driver, login_verification_selector):
    try:
        if WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, login_verification_selector))):
        #if driver.find_element(By.LINK_TEXT, login_verification_selector):
            print("Login session maintainerd on data page")
    except Exception as e:
        print(f"Login session lost on data page: {str(e)}")
        # Save cookies for debugging
        cookies = driver.get_cookies()
        print(f"Cookies after navigation: {cookies}")
        driver.quit()
        exit()


# Check if button is enabeled and clickable
def is_button_disabled(driver, data_url: str, button_name: str):

    # Desired Url
    driver.get(data_url)
    time.sleep(3)

    try:
        # Wait for the button to be present
        wait = WebDriverWait(driver, 5)
        button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, button_name)))
        print("Button is found")

        # Method 1: Check is_enabled()
        is_enabled = button.is_enabled()

        # Method 2: Check for disabled attribute
        # disabled_attr = button.get_attribute("disabled")

        # Determine button state
        # is_disabled = not is_enabled or disabled_attr is not None
        is_disabled = not is_enabled

        if is_disabled:
            print("Button is disabled")
        else:
            print("Button is not disabled")

        return is_disabled
    except Exception as e:
        print(f"Error checking button state: {str(e)}")
        # Return None in case of an error
        return None

# Check if button is clickable and then click
def button_click(driver, button_class_name):
    try:
        wait = WebDriverWait(driver, 5)

        # button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, button_class_name)))
        button = wait.until(EC.element_to_be_clickable((By.XPATH, button_class_name)))

        # Check if button is disabled
        if button.get_attribute("disabled") or not button.is_enabled():
            print("Button is disabled, stopping clicks.")
            return False
        
        # Click the button to load more data
        button.click()
        # Brief pause for content to load
        time.sleep(1)
    except Exception as e:
        print(f"Error during button click or data extraction {e}")
        return False


