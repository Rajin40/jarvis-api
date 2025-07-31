import sys
import json
import uuid
from datetime import datetime
import os

sys.path.append("D:/python/jervis")
from backend.Temperature import temp
from Chrome_Intregretion.CLOCK import what_is_the_time
from Chrome_Intregretion.find_my_ip import find_ip
import webbrowser
from Fiching_email.Google_map_data_scap import scrape_google_maps
from Fiching_email.email_extractor import extract_emails_from_websites
from Fiching_email.Create_json_file import *
from Linkedin_file.automation_Linkedin import main_linkedin
from Linkedin_file.Linkedin_Article_store import analyze_and_store_for_linkedin
from Website_automation.blog_store import analyze_and_store_content_for_website
from Website_automation.post_blog_in_website import post_category_blog
from Generate_code.knowledge_updater import code_gen_mode,list_skills,view_error_log,auto_fix_plugins
from backend.Voice import listen
from data_analysis_tool import data_cleaning
from data_analysis_tool.data_loading import load_excel_data
import pandas as pd

# Session and memory management
MEMORY_FILE = "D:/python/jervis/Data/session_memory.json"
SESSION_FILE = "D:/python/jervis/Data/current_session.json"

# Initialize session memory
def init_memory():
    if not os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'w') as f:
            json.dump({"sessions": []}, f)

# Initialize current session
def init_session():
    if not os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, 'w') as f:
            json.dump({
                "session_id": str(uuid.uuid4()),
                "start_time": datetime.now().isoformat(),
                "actions": [],
                "context": {}
            }, f)

# Load current session
def load_session():
    init_session()
    with open(SESSION_FILE, 'r') as f:
        return json.load(f)

# Save current session
def save_session(session_data):
    with open(SESSION_FILE, 'w') as f:
        json.dump(session_data, f, indent=2)

# Update session memory with completed session
def update_memory(session_data):
    init_memory()
    with open(MEMORY_FILE, 'r+') as f:
        memory = json.load(f)
        memory["sessions"].append(session_data)
        f.seek(0)
        json.dump(memory, f, indent=2)

# Record an action in the session
def record_action(session, cmd, action_type, success, details=None):
    action = {
        "timestamp": datetime.now().isoformat(),
        "command": cmd,
        "type": action_type,
        "success": success,
        "details": details or {}
    }
    session["actions"].append(action)
    save_session(session)
    return session

# simple in-memory storage for current Excel DataFrame
excel_session = {
    "df": None,
    "path": None
}

def split_compound_commands(text):
    """Split compound commands into individual commands"""
    split_words = [" and ", ", ","or", " then ", " after that "]
    commands = text.split(" and ")
    result = []
    for cmd in commands:
        for word in split_words[1:]:
            if word in cmd:
                result.extend(cmd.split(word))
                break
        else:
            result.append(cmd)
    return [cmd.strip() for cmd in result if cmd.strip()]

def Function_cmd(cmd, input_type="text", user_profile=None, context=None):
    # Load or initialize session
    session = load_session()
    
    # Initialize user profile and context if not provided
    if user_profile is None:
        user_profile = {
            "name": "Rajin",
            "language": "en",
            "location": "Dhaka"
        }
    
    if context is None:
        context = {
            "previous_message": "",
            "mode": "command"
        }
    
    # Update session context
    session["user_profile"] = user_profile
    session["context"] = context
    session["last_command"] = cmd
    
    # Split compound commands
    commands = split_compound_commands(cmd.lower())
    
    # Track overall success
    overall_success = False
    
    # Process each command
    for single_cmd in commands:
        success = False
        action_type = "unknown"
        details = {}
        
        # Code Generation
        if any(trigger in single_cmd for trigger in [
            'generate code for', 'create a script for', 'make a python script for',
            'build a program for', 'develop code for', 'write code for',
            'generate plugin for', 'create plugin for', 'make plugin for',
            'code generation for', 'create a python script'
        ]):
            action_type = "code_generation"
            try:
                prompt = single_cmd
                for trigger in [
                    'generate code for', 'create a script for', 'make a python script for',
                    'build a program for', 'develop code for', 'write code for',
                    'generate plugin for', 'create plugin for', 'make plugin for',
                    'code generation for', 'create a python script'
                ]:
                    prompt = prompt.replace(trigger, '')
                prompt = prompt.strip()
                
                if not prompt:
                    print("Please specify what code you want to generate")
                    details = {"error": "No prompt provided"}
                else:
                    print(f"Generating code for: {prompt}")
                    code_gen_mode(prompt, execute=True)
                    list_skills()
                    view_error_log()
                    auto_fix_plugins()
                    success = True
                    details = {"prompt": prompt}
                    
            except Exception as e:
                details = {"error": str(e)}
                print(f"Error during code generation: {str(e)}")

        # LinkedIn Posting
        elif any(trigger in single_cmd for trigger in [
            'do the linkedin post', 'linkedin post', 'post on linkedin',
            'post in linkedin', 'share on linkedin', 'publish to linkedin',
            'create linkedin post', 'make linkedin post', 'post to linkedin now'
        ]):
            action_type = "linkedin_posting"
            try:
                print("Preparing LinkedIn post...")
                success = main_linkedin()
                details = {"success": success}
                if success:
                    print("Successfully posted on LinkedIn")
                else:
                    print("Could not complete the LinkedIn post")
            except Exception as e:
                details = {"error": str(e)}
                print(f"Error while posting to LinkedIn: {str(e)}")

        # Blog Posting
        elif any(trigger in single_cmd for trigger in [
            'post data science blog', 'post data scientist blog', 'publish data science article',
            'post data analysis blog', 'post data analyst blog', 'publish data analysis article',
            'post web development blog', 'post website development blog', 'publish web dev article',
            'post digital marketing blog', 'publish marketing article', 'post digital marketing post',
            'post graphic design blog', 'publish design article', 'post graphics blog',
            'post statistical analysis blog', 'post statistical blog', 'publish stats article',
            'post market research blog', 'publish research article', 'post market research post',
            'post market analysis blog', 'post market analyst blog', 'publish market analysis'
        ]):
            action_type = "blog_posting"
            params = {'status': 'publish', 'index': 0, 'website': False}
            
            if 'as draft' in single_cmd:
                params['status'] = 'draft'
            elif 'as private' in single_cmd:
                params['status'] = 'private'
                
            params['website'] = 'in website' in single_cmd
            
            # Determine category
            category_mapping = {
                'data_science': ['post data science blog', 'post data scientist blog', 'publish data science article'],
                'data_analysis': ['post data analysis blog', 'post data analyst blog', 'publish data analysis article'],
                'web_development': ['post web development blog', 'post website development blog', 'publish web dev article'],
                'digital_marketing': ['post digital marketing blog', 'publish marketing article', 'post digital marketing post'],
                'graphic_design': ['post graphic design blog', 'publish design article', 'post graphics blog'],
                'statistical_analysis': ['post statistical analysis blog', 'post statistical blog', 'publish stats article'],
                'market_research': ['post market research blog', 'publish research article', 'post market research post'],
                'market_analysis': ['post market analysis blog', 'post market analyst blog', 'publish market analysis']
            }
            
            category = None
            for cat, triggers in category_mapping.items():
                if any(trigger in single_cmd for trigger in triggers):
                    category = cat
                    break
                    
            if category:
                try:
                    post_category_blog(category=category, post_index=params['index'], status=params['status'])
                    success = True
                    details = {
                        "category": category,
                        "status": params['status'],
                        "website": params['website']
                    }
                except Exception as e:
                    details = {"error": str(e), "category": category}
            else:
                details = {"error": "Could not determine blog category"}

        # Email Extraction
        elif any(trigger in single_cmd for trigger in [
            'extract emails', 'scrape emails', 'get emails',
            'extract the mails', 'find email addresses', 'collect emails',
            'harvest emails', 'save mails', 'save all email',
            'save emails', 'store emails'
        ]):
            action_type = "email_extraction"
            params = {'immediate': False, 'limit': None, 'domain': None}
            
            if 'now' in single_cmd or 'immediately' in single_cmd:
                params['immediate'] = True
                
            if 'first' in single_cmd:
                params['limit'] = 1
            elif 'top' in single_cmd:
                try:
                    params['limit'] = int(single_cmd.split('top')[1].split()[0])
                except (IndexError, ValueError):
                    params['limit'] = 10
                    
            domain_keywords = ['from', 'for', 'at']
            for keyword in domain_keywords:
                if keyword in single_cmd:
                    parts = single_cmd.split(keyword)
                    if len(parts) > 1:
                        params['domain'] = parts[1].strip().split()[0]
                        break
            
            call_params = {
                'config_path': r'Data\config_json_for_google_map_data.json',
                'output_folder': r"D:\python\jervis\Data"
            }
            
            if params['limit']:
                call_params['limit'] = params['limit']
            if params['domain']:
                call_params['domain'] = params['domain']
            if params['immediate']:
                call_params['immediate'] = True
                
            try:
                extract_emails_from_websites(**call_params)
                success = True
                details = {
                    "limit": params['limit'],
                    "domain": params['domain'],
                    "immediate": params['immediate']
                }
            except Exception as e:
                details = {"error": str(e)}

        # Content Storage
        elif any(trigger in single_cmd for trigger in [
            'store blog for website', 'save blog for website', 'store article for website',
            'save content for website', 'archive post for website'
        ]):
            action_type = "content_storage"
            params = {'immediate': False, 'review': False}
            
            if 'now' in single_cmd or 'immediately' in single_cmd:
                params['immediate'] = True
            if 'review' in single_cmd or 'check first' in single_cmd:
                params['review'] = True
                
            call_params = {
                'chat_log_path': r"D:\python\jervis\Data\ChatLog.json",
                'output_dir': r"D:\python\jervis\Data"
            }
            
            if params['review']:
                call_params['review'] = True
            if params['immediate']:
                call_params['immediate'] = True
                
            try:
                analyze_and_store_content_for_website(**call_params)
                success = True
                details = {
                    "review": params['review'],
                    "immediate": params['immediate']
                }
            except Exception as e:
                details = {"error": str(e)}
                
        elif any(trigger in single_cmd for trigger in [
            'store the article for linkedin', 'save this blog for linkedin',
            'save the article for linkedin', 'store this article for linkedin',
            'archive post for linkedin', 'save for linkedin'
        ]):
            action_type = "linkedin_content_storage"
            params = {'immediate': False, 'review': False}
            
            if 'now' in single_cmd or 'immediately' in single_cmd:
                params['immediate'] = True
            if 'review' in single_cmd or 'check first' in single_cmd:
                params['review'] = True
                
            call_params = {
                'chat_log_path': r"D:\python\jervis\Data\ChatLog.json",
                'output_file_path': r"D:\python\jervis\Data\LinkedInPosts.json"
            }
            
            if params['review']:
                call_params['review'] = True
            if params['immediate']:
                call_params['immediate'] = True
                
            try:
                analyze_and_store_for_linkedin(**call_params)
                success = True
                details = {
                    "review": params['review'],
                    "immediate": params['immediate']
                }
            except Exception as e:
                details = {"error": str(e)}

        # IP Address
        elif "find my ip" in single_cmd or "ip address" in single_cmd:
            action_type = "system_info"
            try:
                ip = find_ip()
                print("your ip is " + ip)
                success = True
                details = {"ip_address": ip}
            except Exception as e:
                details = {"error": str(e)}
        
        # Temperature
        elif "what is the temperature" in single_cmd or "temperature" in single_cmd or "what is temp" in single_cmd:
            action_type = "system_info"
            try:
                temperature = temp()
                success = True
                details = {"temperature": temperature}
            except Exception as e:
                details = {"error": str(e)}
        
        # Excel Work
        elif "excel work" in single_cmd or "excel" in single_cmd:
            action_type = "data_processing"
            try:
                if not excel_session["path"]:
                    file_path = input("Enter full path to Excel file (or drag-drop): ").strip()
                else:
                    use_existing = input(f"Already loaded '{excel_session['path']}'. Use that? (y/n): ").strip().lower()
                    if use_existing == "y":
                        file_path = excel_session["path"]
                    else:
                        file_path = input("Enter new Excel file path: ").strip()

                df = load_excel_data(file_path)
                if df is None:
                    details = {"error": "Failed to load Excel file"}
                else:
                    excel_session["df"] = df
                    excel_session["path"] = file_path
                    success = True
                    details = {
                        "file_path": file_path,
                        "shape": df.shape,
                        "columns": list(df.columns)
                    }
            except Exception as e:
                details = {"error": str(e)}

        # If no command matched
        else:
            action_type = "unknown_command"
            details = {"message": "Command not recognized"}
        
        # Record the action
        session = record_action(session, single_cmd, action_type, success, details)
        
        # Update overall success
        if success:
            overall_success = True
    
    # Update the session end time if this is the last command
    session["last_activity"] = datetime.now().isoformat()
    save_session(session)
    
    return overall_success

# Example usage with full context
Function_cmd("excel work")
    # The session data is automatically saved to SESSION_FILE
    # and will be added to MEMORY_FILE when the session ends






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
#                 print("What type of business or service are you looking for?")
#                 service = listen().lower()
#                 print("And in which location should I search?")
#                 location = listen().lower()
        
#         print(f"Searching for {service} in {location} on Google Maps")
#         results = scrape_google_maps(
#             service=service,
#             location=location,
#             headless=True
#         )
        
#         if results:
#             print(f"I found {len(results)} results for {service} in {location}")
#             for i, result in enumerate(results[:3], 1):  # Read top 3 results
#                 print(f"Result {i}: {result.get('name', 'Unknown')} at {result.get('address', 'unknown address')}")
#         else:
#             print(f"Sorry, I couldn't find any results for {service} in {location}")
            
#     except Exception as e:
#         print("Sorry, I encountered an error while searching Google Maps")
#         print(f"Google Maps search error: {str(e)}")

# # Add this at the bottom of the file
# if __name__ == "__main__":
    
# # Test 1: Full command (text mode simulation)
#     print("=== Testing with full command ===")
#     handle_google_maps_search("search for Businesses in France")
