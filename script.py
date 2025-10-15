import pandas as pd
import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

# --- Configuration ---
CSV_FILE_PATH = 'PraktykiCSV.csv'
CHROME_DEBUG_PORT = "9222"


def round_start_time_down(time_str):
    """Rounds start time down to the nearest 15-minute interval."""
    try:
        t = datetime.strptime(time_str, '%H:%M')
        minutes_to_subtract = t.minute % 15
        if minutes_to_subtract == 0:
            return time_str
        rounded_t = t - timedelta(minutes=minutes_to_subtract)
        return rounded_t.strftime('%H:%M')
    except (ValueError, TypeError):
        print(f"   WARNING: Could not parse time '{time_str}'. Using original value.")
        return time_str

def round_end_time_up(time_str):
    """Rounds end time up to the nearest 15-minute interval."""
    try:
        t = datetime.strptime(time_str, '%H:%M')
        if t.minute % 15 == 0:
            return time_str
        minutes_to_add = 15 - (t.minute % 15)
        rounded_t = t + timedelta(minutes=minutes_to_add)
        return rounded_t.strftime('%H:%M')
    except (ValueError, TypeError):
        print(f"   WARNING: Could not parse time '{time_str}'. Using original value.")
        return time_str

def load_data_from_csv():
    """Loads and validates data from the CSV file."""
    try:
        dataframe = pd.read_csv(CSV_FILE_PATH, sep=',', dtype=str).fillna('')
        required_columns = ['data', 'start', 'end', 'opis']
        if not all(col in dataframe.columns for col in required_columns):
            print(f"ERROR: CSV file must contain the following columns: {required_columns}")
            print(f"Found columns: {list(dataframe.columns)}")
            return None
        print(f"Found {len(dataframe)} entries in the file '{CSV_FILE_PATH}'.")
        return dataframe.to_dict('records')
    except FileNotFoundError:
        print(f"ERROR: File not found '{CSV_FILE_PATH}'. Make sure it's in the same folder as the script.")
        return None

def find_element(wait, by, selector, description):
    """Waits for an element and returns it."""
    print(f"   -> Searching for: {description}")
    try:
        return wait.until(EC.element_to_be_clickable((by, selector)))
    except TimeoutException:
        print(f"   ERROR: Could not find element: {description}")
        return None

def fill_entry_form(driver, entry_data):
    """Fills out the form for a single log entry."""
    wait = WebDriverWait(driver, 10)
    print(f"\n--- Processing entry for date: {entry_data['data']} ---")
    
    rounded_start = round_start_time_down(entry_data.get('start'))
    rounded_end = round_end_time_up(entry_data.get('end'))

    try:
        main_create_button = find_element(wait, By.XPATH, "//button[@title='Utwórz wpis w dzienniku praktyki']", "Main 'Create entry' button")
        if not main_create_button: return False
        main_create_button.click()

        date_field = find_element(wait, By.XPATH, "//lightning-input[@data-field-name='Date__c']//input", "'Date' field")
        if not date_field: return False
        date_field.send_keys(entry_data['data'])

        start_time_field = find_element(wait, By.XPATH, "//lightning-input[@data-field-name='Start_Time__c']//input", "'Start Time' field")
        if not start_time_field: return False
        start_time_field.send_keys(rounded_start)

        end_time_field = find_element(wait, By.XPATH, "//lightning-input[@data-field-name='End_Time__c']//input", "'End Time' field")
        if not end_time_field: return False
        end_time_field.send_keys(rounded_end)

        description_field = find_element(wait, By.XPATH, "//lightning-textarea[@data-field-name='Description__c']//textarea", "'Description' field")
        if not description_field: return False
        description_field.send_keys(entry_data['opis'])

        create_button_in_modal = find_element(wait, By.XPATH, "//div[contains(@class, 'entry__buttons')]//button[@title='Utwórz']", "'Create' button in modal")
        if not create_button_in_modal:
            print("   Could not submit, trying to close modal with ESC key.")
            from selenium.webdriver.common.keys import Keys
            from selenium.webdriver.common.action_chains import ActionChains
            ActionChains(driver).send_keys(Keys.ESCAPE).perform()
            return True
        create_button_in_modal.click()
        
        print(f"--- SUCCESS: Entry for {entry_data['data']} has been submitted. ---")
        time.sleep(3)
        return True

    except Exception as e:
        print(f"   CRITICAL ERROR during processing: {e}")
        return False

def run_automation():
    """Main function to run the entire automation process."""
    data_entries = load_data_from_csv()
    if not data_entries:
        return

    driver = None
    try:
        print("\n" + "="*60)
        print("ACTION REQUIRED: STEP 1 - LAUNCH CHROME IN DEBUG MODE")
        print("See README.md for the exact command for your OS.")
        print(f"Make sure Chrome is running with remote debugging on port {CHROME_DEBUG_PORT}.")
        print("="*60)
        
        print("\n" + "="*60)
        print("ACTION REQUIRED: STEP 2 - PREPARE BROWSER")
        print("In your debug-mode Chrome, log in and navigate to the page with your practice log.")
        print("Once the 'Utwórz wpis w dzienniku praktyki' button is visible...")
        print("Come back here and press ENTER to start the automation.")
        print("="*60)

        input()

        print("\nConnecting to browser and starting automation...\n")
        
        options = Options()
        options.add_experimental_option("debuggerAddress", f"127.0.0.1:{CHROME_DEBUG_PORT}")
        driver = webdriver.Chrome(options=options)
        driver.switch_to.window(driver.current_window_handle)

        for entry in data_entries:
            if not fill_entry_form(driver, entry):
                print("Stopping due to an error.")
                break
        
        print("\nFinished processing all entries.")

    except WebDriverException:
         print(f"\nERROR: Could not connect to Chrome on port {CHROME_DEBUG_PORT}.")
         print("Please check if Chrome is running in debug mode as described in README.md.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if driver:
            print("Automation has finished. The script is detaching from the browser.")
        print("Script has finished.")


if __name__ == "__main__":
    run_automation()

