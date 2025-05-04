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




def handle_linkedin_post(cmd):
    """Function to handle LinkedIn posting commands"""
    
    post_triggers = [
        'do the linkedin post',
        'linkedin post', 
        'post on linkedin',
        'post in linkedin',
        'share on linkedin',
        'publish to linkedin',
        'create linkedin post',
        'make linkedin post',
        'post to linkedin now'
    ]
    
    if any(trigger in cmd for trigger in post_triggers):
        try:
            speak("Preparing LinkedIn post...")
            success = main_linkedin()
            
            if success:
                speak("Successfully posted on LinkedIn")
                print("LinkedIn post completed successfully")
                return True
            else:
                speak("Could not complete the LinkedIn post")
                print("LinkedIn post failed")
                return False
                
        except Exception as e:
            error_msg = f"Error while posting to LinkedIn: {str(e)}"
            speak(error_msg)
            print(error_msg)
            return False
            
    return False



def handle_blog_posting(cmd):
    """Advanced function to handle blog posting commands"""
    
    # Define all blog categories and their possible command triggers
    blog_categories = {
        'data_science': [
            'post data science blog',
            'post data scientist blog',
            'publish data science article'
        ],
        'data_analysis': [
            'post data analysis blog',
            'post data analyst blog',
            'publish data analysis article'
        ],
        'web_development': [
            'post web development blog',
            'post website development blog',
            'publish web dev article'
        ],
        'digital_marketing': [
            'post digital marketing blog',
            'publish marketing article',
            'post digital marketing post'
        ],
        'graphic_design': [
            'post graphic design blog',
            'publish design article',
            'post graphics blog'
        ],
        'statistical_analysis': [
            'post statistical analysis blog',
            'post statistical blog',
            'publish stats article'
        ],
        'market_research': [
            'post market research blog',
            'publish research article',
            'post market research post'
        ],
        'market_analysis': [
            'post market analysis blog',
            'post market analyst blog',
            'publish market analysis'
        ]
    }
    
    # Additional parameters that can be specified
    params = {
        'status': 'publish',  # default status
        'index': 0,          # default post index
        'website': False      # whether to specify "in website"
    }
    
    # Check for status keywords
    if 'as draft' in cmd:
        params['status'] = 'draft'
    elif 'as private' in cmd:
        params['status'] = 'private'
    
    # Check if "in website" is specified
    params['website'] = 'in website' in cmd
    
    # Find which category is being requested
    for category, triggers in blog_categories.items():
        if any(trigger in cmd for trigger in triggers):
            # Call the posting function with collected parameters
            post_category_blog(
                category=category,
                post_index=params['index'],
                status=params['status']
            )
            return True  # Indicate we handled a blog post command
    
    return False  # No blog post command was found

def handle_email_extraction(cmd):
    """Advanced function to handle email extraction commands"""
    
    # Define email extraction parameters
    extraction_commands = {
        'triggers': [
        'extract emails',
        'scrape emails',
        'get emails',
        'extract the mails',
        'find email addresses',
        'collect emails',
        'harvest emails',
        'save mails',          # New trigger
        'save all email',      # New trigger
        'save emails',         # New trigger
        'store emails'         # New trigger
    ],
        'function': extract_emails_from_websites,
        'default_params': {
            'config_path': r'Data\config_json_for_google_map_data.json',
            'output_folder': r"D:\python\jervis\Data"
        }
    }
    
    # Additional parameters that can be specified
    params = {
        'immediate': False,    # whether to process immediately
        'limit': None,         # number of emails to extract
        'domain': None        # specific domain to target
    }
    
    # Check for processing options
    if 'now' in cmd or 'immediately' in cmd:
        params['immediate'] = True
    
    # Check for extraction limits
    if 'first' in cmd:
        params['limit'] = 1
    elif 'top' in cmd:
        # Extract number after 'top' (e.g., "top 10 emails")
        try:
            params['limit'] = int(cmd.split('top')[1].split()[0])
        except (IndexError, ValueError):
            params['limit'] = 10
    
    # Check for specific domain
    domain_keywords = ['from', 'for', 'at']
    for keyword in domain_keywords:
        if keyword in cmd:
            # Try to extract domain (e.g., "extract emails from gmail.com")
            parts = cmd.split(keyword)
            if len(parts) > 1:
                params['domain'] = parts[1].strip().split()[0]
                break
    
    # Check if this is an email extraction command
    if any(trigger in cmd for trigger in extraction_commands['triggers']):
        # Prepare parameters
        call_params = extraction_commands['default_params'].copy()
        
        # Add additional parameters if needed by the function
        if params['limit']:
            call_params['limit'] = params['limit']
        if params['domain']:
            call_params['domain'] = params['domain']
        if params['immediate']:
            call_params['immediate'] = True
        
        # Call the extraction function with collected parameters
        extraction_commands['function'](**call_params)
        return True  # Indicate we handled an extraction command
    
    return False  # No extraction command was found


def handle_content_storage(cmd):
    """Advanced function to handle content storage commands"""
    
    # Define all storage targets and their possible command triggers
    storage_targets = {
        'website': {
            'triggers': [
                'store blog for website',
                'save blog for website',
                'store article for website',
                'save content for website',
                'archive post for website'
            ],
            'function': analyze_and_store_content_for_website,
            'default_params': {
                'chat_log_path': r"D:\python\jervis\Data\ChatLog.json",
                'output_dir': r"D:\python\jervis\Data"
            }
        },
        'linkedin': {
            'triggers': [
                'store the article for linkedin',
                'save this blog for linkedin',
                'save the article for linkedin',
                'store this article for linkedin',
                'archive post for linkedin',
                'save for linkedin'
            ],
            'function': analyze_and_store_for_linkedin,
            'default_params': {
                'chat_log_path': r"D:\python\jervis\Data\ChatLog.json",
                'output_file_path': r"D:\python\jervis\Data\LinkedInPosts.json"
            }
        }
    }
    
    # Additional parameters that can be specified
    params = {
        'immediate': False,    # whether to process immediately
        'review': False        # whether to review before saving
    }
    
    # Check for processing options
    if 'now' in cmd or 'immediately' in cmd:
        params['immediate'] = True
    if 'review' in cmd or 'check first' in cmd:
        params['review'] = True
    
    # Find which storage target is being requested
    for target, config in storage_targets.items():
        if any(trigger in cmd for trigger in config['triggers']):
            # Prepare parameters
            call_params = config['default_params'].copy()
            
            # Add additional parameters if needed by the function
            if params['review']:
                call_params['review'] = True
            if params['immediate']:
                call_params['immediate'] = True
            
            # Call the storage function with collected parameters
            config['function'](**call_params)
            return True  # Indicate we handled a storage command
    
    return False  # No storage command was found



def handle_volume_control(cmd):
    """Advanced function to handle volume control commands"""
    
    volume_actions = {
        'increase': {
            'triggers': [
                'increase volume',
                'volume up',
                'volume badhao',
                'increase sound',
                'louder',
                'sound badhao'
            ],
            'key': 'volumeup',
            'press_count': 4,
            'response': "Volume increased."
        },
        'decrease': {
            'triggers': [
                'decrease volume',
                'volume down', 
                'volume kam karo',
                'decrease sound',
                'quieter',
                'sound kam karo'
            ],
            'key': 'volumedown',
            'press_count': 4,
            'response': "Volume decreased."
        },
        'max': {
            'triggers': [
                'full volume',
                'full volume kr do',
                'maximum volume',
                'volume full karo',
                '100% volume'
            ],
            'key': 'volumeup',
            'press_count': 20,
            'response': "Now your system is at full volume boss"
        },
        'mute': {
            'triggers': [
                'mute',
                'mute volume',
                'sound off',
                'volume band karo'
            ],
            'key': 'volumemute',
            'press_count': 1,
            'response': "Volume muted."
        }
    }

    # Find matching volume action
    for action, config in volume_actions.items():
        if any(trigger in cmd for trigger in config['triggers']):
            # Press the key the specified number of times
            for _ in range(config['press_count']):
                gui.press(config['key'])
            
            # Provide feedback
            if 'speak' in globals():  # Check if speak function exists
                speak(config['response'])
            print(config['response'])
            return True
            
    return False


def handle_browser_system_controls(cmd):
    """Advanced function to handle browser and system control commands"""
    
    controls = {
        # Website navigation
        'visit': {
            'triggers': ['visit', 'launch', 'open website'],
            'action': lambda: webbrowser.open(f"https://www.{cmd.split()[-1]}.com"),
            'response': f"Visiting {cmd.split()[-1]}"
        },
        
        # Media controls
        'media': {
            'play_pause': {
                'triggers': ['play', 'pause', 'stop'],
                'action': lambda: gui.hotkey("space"),
                'response': "Media control executed"
            }
        },
        
        # Window management
        'window': {
            'maximize': {
                'triggers': ['maximize window', 'maximize this'],
                'action': lambda: gui.hotkey("win", "up"),
                'response': "Maximizing window"
            },
            'minimise': {
                'triggers': ['minimise window', 'minimise this','minimize it"'],
                'action': lambda: gui.hotkey("win", "up"),
                'response': "Maximizing window"
            },
            'restore': {
                'triggers': ['restore window'],
                'action': lambda: gui.hotkey("win", "shift", "up"),
                'response': "Restoring window"
            },
            'switch': {
                'triggers': ['switch window', 'next window'],
                'action': lambda: gui.hotkey("alt", "tab"),
                'response': "Switching to next window"
            },
            'previous': {
                'triggers': ['previous window', 'back window'],
                'action': lambda: gui.hotkey("alt", "shift", "tab"),
                'response': "Switching to previous window"
            }
        },
        
        # Browser controls
        'browser': {
            'incognito': {
                'triggers': ['open incognito', 'private window'],
                'action': lambda: gui.hotkey("ctrl", "shift", "n"),
                'response': "Opening incognito window"
            },
            'bookmark': {
                'triggers': ['bookmark page', 'save page'],
                'action': lambda: gui.hotkey("ctrl", "d"),
                'response': "Bookmarking page"
            },
            # ... (add all other browser controls in this structure)
        },
        
        # System controls
        'system': {
            'shutdown': {
                'triggers': ['shutdown', 'turn off computer'],
                'action': lambda: [
                    gui.hotkey("win","d"),
                    time.sleep(0.4),
                    gui.hotkey("alt", "f4"),
                    time.sleep(0.4),
                    gui.press("enter")
                ],
                'response': "Shutting down"
            },
            # ... (add all other system controls in this structure)
        }
    }

    # Search for matching control
    for category, actions in controls.items():
        if isinstance(actions, dict):  # For nested categories
            for action_name, config in actions.items():
                if any(trigger in cmd for trigger in config['triggers']):
                    config['action']()
                    if 'speak' in globals():
                        speak(config['response'])
                    print(config['response'])
                    return True
        else:  # For top-level actions like 'visit'
            if any(trigger in cmd for trigger in actions['triggers']):
                actions['action']()
                if 'speak' in globals():
                    speak(actions['response'])
                print(actions['response'])
                return True
                
    return False

def handle_text_editing(cmd):
    """Advanced function to handle text input and editing commands"""
    
    text_actions = {
        'write': {
            'triggers': ['write', 'type'],
            'action': lambda: (
                speak("writing boss"),
                gui.write(cmd.replace("write", "").replace("type", "").strip())
            ),
            'response': "Text written"
        },
        'enter': {
            'triggers': ['enter', 'press enter'],
            'action': lambda: gui.press("enter"),
            'response': "Enter pressed"
        },
        'select_all': {
            'triggers': ['select all', 'select all this'],
            'action': lambda: (
                speak("done boss"),
                gui.hotkey("ctrl", "a")
            ),
            'response': "All content selected"
        },
        'copy': {
            'triggers': ['copy', 'copy this'],
            'action': lambda: gui.hotkey("ctrl", "c"),
            'response': "Content copied"
        },
        'paste': {
            'triggers': ['paste', 'paste here'],
            'action': lambda: gui.hotkey("ctrl", "v"),
            'response': "Content pasted"
        },
        'undo': {
            'triggers': ['undo', 'undo karo', 'back', 'back karo'],
            'action': lambda: gui.hotkey("ctrl", "z"),
            'response': "Action undone"
        },
        'cut': {
            'triggers': ['cut', 'cut this'],
            'action': lambda: gui.hotkey("ctrl", "x"),
            'response': "Content cut"
        },
        'redo': {
            'triggers': ['redo', 'redo karo', 'forward', 'forward karo'],
            'action': lambda: gui.hotkey("ctrl", "y"),
            'response': "Action redone"
        },
        'delete': {
            'triggers': ['delete', 'delete this'],
            'action': lambda: gui.press("delete"),
            'response': "Content deleted"
        },
        'backspace': {
            'triggers': ['backspace', 'remove'],
            'action': lambda: gui.press("backspace"),
            'response': "Character removed"
        }
    }

    # Find matching text action
    for action, config in text_actions.items():
        if any(trigger in cmd for trigger in config['triggers']):
            config['action']()
            if 'speak' in globals() and 'response' in config:
                speak(config['response'])
            print(config.get('response', 'Action completed'))
            return True
            
    return False
































# def handle_google_maps_search(text):
#     try:
#         # Check if the query already contains the service and location
#         if "search for" in text and "in" in text:
#             parts = text.split("search for")[1].split("in")
#             service = parts[0].strip()
#             location = parts[1].strip()
#         elif "find" in text and "in" in text:
#             parts = text.split("find")[1].split("in")
#             service = parts[0].strip()
#             location = parts[1].strip()
#         else:
#             print("\nHow would you like to provide the search details?")
#             print("1. Type the information")
#             print("2. Speak the information")
            
#             while True:
#                 choice = input("Enter your choice (1 or 2): ").strip()
#                 if choice in ['1', '2']:
#                     break
#                 print("Invalid choice. Please enter 1 or 2.")
            
#             if choice == '1':
#                 service = input("What type of business or service are you looking for? ").strip()
#                 location = input("In which location should I search? ").strip()
#             else:
#                 speak("What type of business or service are you looking for?")
#                 service = listen().lower()
#                 speak("And in which location should I search?")
#                 location = listen().lower()
        
#         speak(f"Searching for {service} in {location} on Google Maps")
#         results = scrape_google_maps(
#             service=service,
#             location=location,
#             headless=True
#         )
        
#         if results:
#             speak(f"I found {len(results)} results for {service} in {location}")
#             for i, result in enumerate(results[:3], 1):  # Read top 3 results
#                 speak(f"Result {i}: {result.get('name', 'Unknown')} at {result.get('address', 'unknown address')}")
#         else:
#             speak(f"Sorry, I couldn't find any results for {service} in {location}")
            
#     except Exception as e:
#         speak("Sorry, I encountered an error while searching Google Maps")
#         print(f"Google Maps search error: {str(e)}")

# Add this at the bottom of the file
#if __name__ == "__main__":
    
# Test 1: Full command (text mode simulation)
    #print("=== Testing with full command ===")
    #handle_google_maps_search("search for Businesses in France")