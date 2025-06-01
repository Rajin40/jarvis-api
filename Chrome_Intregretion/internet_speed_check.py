from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
import time
import sys
sys.path.append("D:/python/jervis")
from backend.british_brian_Voice import speak # Import the voice module

def get_internet_speed():
    # Set the path to your ChromeDriver executable
    chrome_driver_path = r"C:\Users\alifb\OneDrive\Pictures\New folder\chromedriver-win64\chromedriver.exe"
    
    # Set Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")  # Disable GPU for headless mode
    chrome_options.add_argument("--no-sandbox")  # Disable sandbox for permissions

    # Initialize Chrome browser in headless mode
    service = ChromeService(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Open the Fast.com website
        driver.get('https://fast.com/')
        speak("Checking your internet speed...")
        
        # Wait for the page to load (using time.sleep)
        time.sleep(10)  # Allow time for the speed value to load dynamically

        # Find the element with the speed value
        speed_element = driver.find_element(By.ID, 'speed-value')
        
        # Get the text value from the element
        speed_value = speed_element.text

        # Return the speed value
        return speed_value
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        # Ensure the driver quits to release resources
        driver.quit()

def check_internet_speed():
    speed_result = get_internet_speed()

    if speed_result is not None:
        speak(f"Sir, your internet speed is: {speed_result} Mbps")
    else:
        speak("Error: Unable to retrieve internet speed.")

