import time
import schedule  # For post scheduling
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc
from British_Brian_Voice import speak

# Configuration
LOGIN_URL = "https://www.facebook.com/login"
USERNAME = "01902700852"
PASSWORD = "Akalam@#@019027@#"
HOME_URL = "https://www.facebook.com/"
MESSAGES_URL = "https://www.facebook.com/messages/t/"

def setup_driver():
    """Initialize and return an undetected Chrome WebDriver instance."""
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = uc.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def login(driver):
    """Log into Facebook."""
    driver.get(LOGIN_URL)
    speak("Logging into Facebook.")
    driver.find_element(By.ID, "email").send_keys(USERNAME)
    driver.find_element(By.ID, "pass").send_keys(PASSWORD)
    driver.find_element(By.NAME, "login").click()
    time.sleep(5)
    if "facebook.com" in driver.current_url:
        speak("Login successful.")
    else:
        speak("Login failed. Please check your credentials.")

def handle_messages(driver):
    """Automate Facebook message handling and replies."""
    speak("Checking Facebook messages.")
    driver.get(MESSAGES_URL)
    time.sleep(5)
    
    try:
        unread_messages = driver.find_elements(By.CLASS_NAME, "j_3d")
        if unread_messages:
            speak(f"You have {len(unread_messages)} unread messages.")
            for message in unread_messages:
                message.click()
                time.sleep(3)
                last_message = driver.find_elements(By.CLASS_NAME, "hidden_elem")[-1].text
                speak(f"New message: {last_message}. Would you like to reply?")
                response = input("Do you want to reply? (yes/no): ").strip().lower()
                if response == "yes":
                    reply = input("Enter your reply: ")
                    reply_box = driver.find_element(By.CLASS_NAME, "notranslate")
                    reply_box.send_keys(reply, Keys.ENTER)
                    speak("Reply sent.")
                else:
                    speak("Skipping this message.")
        else:
            speak("No unread messages.")
    except Exception as e:
        speak(f"An error occurred while handling messages: {e}")

def post_content(driver, content):
    """Post content on Facebook's feed."""
    speak("Preparing to post on Facebook.")
    driver.get(HOME_URL)
    time.sleep(5)
    try:
        post_box = driver.find_element(By.CLASS_NAME, "_5rpb")
        post_box.click()
        time.sleep(2)
        text_area = driver.find_element(By.CLASS_NAME, "notranslate")
        text_area.send_keys(content)
        post_button = driver.find_element(By.XPATH, "//button[contains(@data-testid, 'react-composer-post-button')]")
        post_button.click()
        speak("Post published successfully.")
    except Exception as e:
        speak(f"Failed to post: {e}")

def ask_before_post(driver, content):
    """Ask user for confirmation before posting. If no response, auto-post after a delay."""
    speak("Would you like to post the following message on Facebook?")
    print(f"Content: {content}")
    response = input("Post this content? (yes/no) (Auto-posting in 15 seconds): ").strip().lower()
    
    def auto_post():
        speak("No response received. Auto-posting now.")
        post_content(driver, content)
    
    time.sleep(15)  # Wait for user input
    if response == "yes":
        post_content(driver, content)
    elif response == "no":
        speak("Post canceled.")
    else:
        auto_post()

def schedule_posts(driver):
    """Schedule posts at specified times automatically."""
    post_times = ["10:00", "14:00"]  # Define your post times
    scheduled_content = ["Morning inspiration!", "Afternoon update!"]
    
    for time_slot, content in zip(post_times, scheduled_content):
        schedule.every().day.at(time_slot).do(post_content, driver, content)
    
    speak("Scheduled posting enabled.")
    while True:
        schedule.run_pending()
        time.sleep(1)

def main():
    """Main function to run the Facebook automation."""
    driver = setup_driver()
    try:
        login(driver)
        while True:
            speak("Would you like to check messages or post content? (Enter 'messages' or 'post')")
            user_choice = input("Choose an option (messages/post/schedule): ").strip().lower()
            if user_choice == "messages":
                handle_messages(driver)
            elif user_choice == "post":
                content = input("Enter the content you want to post: ")
                ask_before_post(driver, content)
            elif user_choice == "schedule":
                schedule_posts(driver)
            else:
                speak("Invalid option. Please try again.")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
