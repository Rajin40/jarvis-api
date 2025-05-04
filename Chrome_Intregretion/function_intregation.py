import sys
sys.path.append("D:/python/jervis")
from Temperature import temp
from backend.British_Brian_Voice import speak  # Import the voice module
from Internet_speed_check import *
from check_online_offline import *
from clap_with_music import *
from CLOCK import *
from find_my_ip import *
from seo_generator import *
from open_everything.open_auto import open_multiple_items
from close_eveything.colse_auto import *
import pyautogui as gui
import webbrowser
from Fiching_email.Google_map_data_scap import scrape_google_maps
from backend.Voice import listen
from Fiching_email.email_extractor import extract_emails_from_websites
from Fiching_email.Create_json_file import *
from Fiching_email.Email_sender import main
from Linkedin_file.automation_Linkedin import main_linkedin
from Linkedin_file.Linkedin_Article_store import analyze_and_store_for_linkedin
from Website_automation.blog_store import analyze_and_store_content_for_website
from Website_automation.post_blog_in_website import post_category_blog
from backend.Chatbot import ChatBot
from Chrome_Intregretion.function_store import *
import json
from datetime import datetime

# Add this function to handle command logging
def log_structured_command(action, details, method="voice", user_response="positive"):
    """
    Logs a command execution to a JSON file.
    
    Args:
        action (str): The type of action performed (e.g., "open_app", "internet_speed_test")
        details (dict): Specific details about the action
        method (str): How the command was initiated ("voice" or "manual")
        user_response (str): User's response to the action ("positive", "neutral", "negative")
    """
    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "action": action,
        "details": details,
        "method": method,
        "user_response": user_response
    }
    
    # Append to a log file
    try:
        with open(r"D:\python\jervis\Data\store_function_behavior\command_logs.json", "a") as f:
            f.write(json.dumps(log_entry) + "\n")
    except Exception as e:
        print(f"Error logging command: {e}")


def split_compound_commands(text):
    """Split compound commands into individual commands"""
    # Common conjunctions to split on
    split_words = [" and ", ", ","or", " then ", " after that "]
    
    # First split on the most common conjunction
    commands = text.split(" and ")
    
    # Further split if other conjunctions were used
    result = []
    for cmd in commands:
        for word in split_words[1:]:
            if word in cmd:
                result.extend(cmd.split(word))
                break
        else:
            result.append(cmd)
    
    # Clean up each command
    return [cmd.strip() for cmd in result if cmd.strip()]

def Function_cmd(text):
    # Split compound commands
    commands = split_compound_commands(text.lower())
    
    # Process each command
    for cmd in commands:
        try:
            print(f"Processing command: {cmd}")  # Debug logging
            
            # Initialize variables for structured logging
            action = None
            details = {"raw_command": cmd}
            user_response = None
            
            # Your existing command processing logic with added structured logging
            if "check internet speed" in cmd or "check speed test" in cmd or "speed test" in cmd:
                action = "check_internet_speed"
                log_structured_command(action, details)
                check_internet_speed()


            elif handle_linkedin_post(cmd):
                action = "linkedin_posting"
                log_structured_command(action, details)
                continue

            elif handle_blog_posting(cmd):
                action = "blog_posting"
                log_structured_command(action, details)
                continue

            elif handle_content_storage(cmd):
                action = "content_storage"
                log_structured_command(action, details)
                continue

            elif handle_email_extraction(cmd):
                action = "email_extraction"
                log_structured_command(action, details)
                continue

            elif any(keyword in cmd for keyword in ["generate"]):
                action = "generate_content"
                query = cmd.replace("generate", "").strip()
                details["query"] = query
                log_structured_command(action, details)
                ChatBot(Query=query)

            elif "find my ip" in cmd or "ip address" in cmd:
                action = "find_ip"
                log_structured_command(action, details)
                speak("your ip is " + find_ip())

            elif "are you offline" in cmd or "hello there" in cmd:
                action = "check_internet_status"
                log_structured_command(action, details)
                internet_status()

            elif "what is the time" in text or "time" in text or "what time is" in text:
                action = "check_time"
                log_structured_command(action, details)
                what_is_the_time()

            elif "start clap with music system" in text or "start smart music system" in text:
                action = "start_music_system"
                log_structured_command(action, details)
                speak("ok now starting")
                clap_to_misuc()

            elif text.startswith(("open","kholo","show me")):
                action = "open_application"
                text = text.replace("kholo","")
                text = text.replace("show me","")
                text = text.strip()
                details["app_name"] = text
                log_structured_command(action, details)
                open_multiple_items(text)

            elif handle_text_editing(cmd):
                action = "text_editing"
                log_structured_command(action, details)
                continue

            elif handle_volume_control(cmd):
                action = "volume_control"
                log_structured_command(action, details)
                continue

            elif handle_browser_system_controls(cmd):
                action = "browser_control"
                log_structured_command(action, details)
                continue

            elif "do the linkedin post" in text or "linkedin post" in text or "post on linkedin" in text or "post in linkedin" in text:
                action = "linkedin_post"
                try:
                    log_structured_command(action, details)
                    success = main_linkedin()
                    
                    if success:
                        speak("Successfully posted on LinkedIn")
                        user_response = "positive"
                    else:
                        speak("Failed to complete LinkedIn post")
                        user_response = "negative"
                    
                    # Update the log with user response
                    log_structured_command(action, details, user_response=user_response)
                    return success
                        
                except Exception as e:
                    speak(f"Error executing LinkedIn post: {str(e)}")
                    user_response = "error"
                    log_structured_command(action, details, user_response=user_response)
                    return False
            
        except Exception as e:
            speak(f"Sorry, I had trouble with: {cmd}")
            print(f"Error processing '{cmd}': {e}")
            # Log the failed command
            log_structured_command("command_failed", {"raw_command": cmd, "error": str(e)})

Function_cmd("what is the time")











