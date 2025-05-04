from open_everything.open_auto import open  # Import your custom `open` function
import sys
sys.path.append("D:/python/jervis")
from backend.British_Brian_Voice import speak  # Import the voice module
import time
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc

def open_fiverr_website():
    """Open Fiverr website."""
    speak("Opening Fiverr website.")
    open("open fiverr website")

from British_Brian_Voice import speak


MESSAGE_URL = open("open fiverr inbox website")


def check_fiverr_messages():
    """Open Fiverr inbox and fetch unread messages."""
    driver = uc.Chrome(service=(ChromeDriverManager().install()))
    try:
        speak("Opening Fiverr inbox.")
        driver.get(MESSAGE_URL)
        time.sleep(10)  # Allow the inbox to load
        unread_messages = driver.find_elements(By.CSS_SELECTOR, ".conversation-item-container")
        if unread_messages:
            speak(f"You have {len(unread_messages)} unread messages.")
            return driver, unread_messages
        else:
            speak("No unread messages.")
            driver.quit()
            return None, []
    except Exception as e:
        speak(f"An error occurred: {e}")
        if 'driver' in locals():
            driver.quit()
        return None, []


def handle_unread_messages(driver, unread_messages):
    """Process each unread message."""
    for message in unread_messages:
        try:
            message.click()
            time.sleep(3)
            messages = driver.find_elements(By.CSS_SELECTOR, ".conversation-message")
            last_message = messages[-1].text if messages else "No content found."
            speak(f"Client said: {last_message}")
            yield last_message
        except Exception as e:
            speak(f"An error occurred while processing a message: {e}")


import json
def load_qa_pairs(file_path="qa_pairs.json"):
    """Load predefined question-answer pairs."""
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_qa_pairs(qa_pairs, file_path="qa_pairs.json"):
    """Save updated question-answer pairs."""
    with open(file_path, "w") as file:
        json.dump(qa_pairs, file, indent=4)




def reply_to_message(driver, message, qa_pairs):
    """Reply to a message based on predefined or user-provided answers."""
    auto_reply = qa_pairs.get(message.lower())
    reply_box = driver.find_element(By.CSS_SELECTOR, ".reply-box-textarea")

    if auto_reply:
        speak(f"Auto-replying: {auto_reply}")
        reply_box.send_keys(auto_reply)
        reply_box.send_keys(Keys.ENTER)
        speak("Auto-reply sent.")
    else:
        speak("No predefined answer found. Please provide a reply.")
        manual_reply = input("Enter your reply: ").strip()
        reply_box.send_keys(manual_reply)
        reply_box.send_keys(Keys.ENTER)
        speak("Manual reply sent.")

        save_pair = input("Do you want to save this question and answer for future use? (yes/no): ").strip().lower()
        if save_pair == "yes":
            qa_pairs[message.lower()] = manual_reply
            save_qa_pairs(qa_pairs)
            speak("Question and answer saved.")

def main():
    open_fiverr_website()
    driver, unread_messages = check_fiverr_messages()
    
    if unread_messages:
        qa_pairs = load_qa_pairs()
        for message in handle_unread_messages(driver, unread_messages):
            reply_to_message(driver, message, qa_pairs)
    
    if 'driver' in locals():
        driver.quit()

if __name__ == "__main__":
    main()
