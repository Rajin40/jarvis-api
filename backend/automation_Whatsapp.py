import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import sys
sys.path.append("D:/python/jervis")
from open_everything.open_auto import open  # Importing your `open` function
from British_Brian_Voice import speak
MESSAGE_URL ="https://web.whatsapp.com/"
def handle_messages(driver):
    """Automate LinkedIn message handling and replies with enhanced interaction."""
    speak("Checking LinkedIn messages.")
    driver.get(MESSAGE_URL)
    time.sleep(5)
    
    try:
        unread_messages = driver.find_elements(By.CLASS_NAME, "msg-conversation-listitem__link")
        unread_count = len(unread_messages)

        if unread_count > 0:
            speak(f"You have {unread_count} unread messages.")
            response = input("Can I tell you the names of the senders? (yes/no): ").strip().lower()

            if response == "yes":
                message_names = []
                for message in unread_messages:
                    try:
                        # Extract the sender's name
                        name_element = message.find_element(By.CSS_SELECTOR, ".msg-conversation-listitem__participant-names")
                        sender_name = name_element.text.strip()
                        message_names.append(sender_name)
                        speak(f"Message from {sender_name}")
                    except Exception as e:
                        speak("Could not extract the sender's name.")
                        print(f"Error extracting name: {e}")

                specific_response = input("Do you want to see any specific person's message? (yes/no): ").strip().lower()
                if specific_response == "yes":
                    person_name = input("Enter the name of the person: ").strip()
                    found = False
                    for message in unread_messages:
                        name_element = message.find_element(By.CSS_SELECTOR, ".msg-conversation-listitem__participant-names")
                        if person_name.lower() in name_element.text.lower():
                            found = True
                            message.click()
                            time.sleep(3)
                            last_message = driver.find_elements(By.CLASS_NAME, "msg-s-message-list__event")[-1].text
                            speak(f"The last message from {name_element.text} is: {last_message}.")
                            if input("Do you want to reply? (yes/no): ").strip().lower() == "yes":
                                reply = input("Enter your reply: ")
                                reply_box = driver.find_element(By.CLASS_NAME, "msg-form__contenteditable")
                                reply_box.send_keys(reply, Keys.ENTER)
                                speak("Reply sent.")
                            break
                    if not found:
                        speak(f"No messages found from {person_name}.")
                else:
                    speak("Skipping specific messages.")
            else:
                speak("Skipping name announcement.")

            speak("Do you want to hear all messages?")
            final_response = input("Options: 'yes', 'no', 'skip all': ").strip().lower()
            if final_response == "yes":
                for i, message in enumerate(unread_messages):
                    message.click()
                    time.sleep(3)
                    last_message = driver.find_elements(By.CLASS_NAME, "msg-s-message-list__event")[-1].text
                    name = message.find_element(By.CSS_SELECTOR, ".msg-conversation-listitem__participant-names").text
                    speak(f"Message {i+1} from {name}: {last_message}")
                    if input("Do you want to reply? (yes/no/skip): ").strip().lower() == "yes":
                        reply = input("Enter your reply: ")
                        reply_box = driver.find_element(By.CLASS_NAME, "msg-form__contenteditable")
                        reply_box.send_keys(reply, Keys.ENTER)
                        speak("Reply sent.")
            elif final_response == "skip all":
                speak("Skipping all messages.")
            else:
                speak("No more messages will be read.")
        else:
            speak("No unread messages.")
    except Exception as e:
        speak(f"An error occurred while handling messages: {e}")

def open_whatsapp():
    """Use `open_auto` to open WhatsApp Web."""
    speak("Opening WhatsApp Web.")
    open("open whatsapp website")
    time.sleep(5)  # Wait for QR code scanning or loading

def main():
    """Main function for WhatsApp automation."""
    try:
        open_whatsapp()
        while True:
            speak("Would you like to handle chats?")
            user_choice = input("Choose an option (handle/exit): ").strip().lower()
            if user_choice == "handle":
                from selenium import webdriver
                driver = webdriver.Chrome()  # Make sure you have the driver initialized
                handle_messages(driver)
            elif user_choice == "exit":
                speak("Exiting WhatsApp automation.")
                break
            else:
                speak("Invalid option. Please try again.")
    except Exception as e:
        speak(f"An error occurred: {e}")

# Uncomment the below lines to run the script
if __name__ == "__main__":
    main()
