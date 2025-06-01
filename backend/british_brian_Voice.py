# import time
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import undetected_chromedriver as uc

# chrome_options = uc.ChromeOptions()
# chrome_options.add_argument("--headless")  # Run in headless mode (without opening a browser window)

# # Create a Chrome driver instance with the specified options
# driver = webdriver.Chrome(options=chrome_options)

# # Navigate to the website
# driver.get("https://tts.5e7en.me/")

# # Navigate to the website

# def speak(text):
#     try:
#         # Wait for the element to be clickable
#         element_to_click = WebDriverWait(driver,5).until(
#             EC.element_to_be_clickable((By.XPATH,'//*[@id="text"]'))
#         )
#         # Perform the click action
#         element_to_click.click()
#         # Input text into the element
#         text_to_input = text
#         element_to_click.send_keys(text_to_input)
#         print (text_to_input)
#         # Calculate sleep duration based on sentence length
#         sleep_duration = min(1 + len(text) // 13, 50)
#         # Minimum sleep is 3 seconds, maximum is 10 seconds
#         # Wait for the button to be clickable
#         button_to_click = WebDriverWait(driver,2).until(
#             EC.element_to_be_clickable((By.XPATH,
#                 '//*[@id="button"]')))
#         # Perform the click action on the button
#         button_to_click.click()

#         # Sleep for dynamically calculated duration
#         time.sleep (sleep_duration)

#         # Clear the text box for the next sentence
#         element_to_click.clear()
        
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         # Handle the error as needed, e.g., log it, raise it again, etc.

import pyttsx3

# Initialize the TTS engine
engine = pyttsx3.init()

def speak(text, rate=150, volume=1.0, voice=None):
    """
    Advanced text-to-speech function using pyttsx3
    
    Parameters:
    - text: The text to speak
    - rate: Words per minute (default 150)
    - volume: Volume level between 0.0 and 1.0 (default 1.0)
    - voice: Optional specific voice ID to use
    """
    try:
        # Set properties
        engine.setProperty('rate', rate)
        engine.setProperty('volume', volume)
        
        # Set voice if specified
        if voice:
            voices = engine.getProperty('voices')
            if voice < len(voices):
                engine.setProperty('voice', voices[voice].id)
        
        # Speak the text
        engine.say(text)
        engine.runAndWait()
        
    except Exception as e:
        print(f"An error occurred: {e}")

