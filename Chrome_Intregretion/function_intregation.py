import sys
sys.path.append("D:/python/jervis")
from backend.Temperature import temp
from Chrome_Intregretion.CLOCK import what_is_the_time
from Chrome_Intregretion.find_my_ip import *
import pyautogui as gui
import webbrowser
from Fiching_email.Google_map_data_scap import scrape_google_maps
from Fiching_email.email_extractor import extract_emails_from_websites
from Fiching_email.Create_json_file import *
from Linkedin_file.automation_Linkedin import main_linkedin
from Linkedin_file.Linkedin_Article_store import analyze_and_store_for_linkedin
from Website_automation.blog_store import analyze_and_store_content_for_website
from Website_automation.post_blog_in_website import post_category_blog
from Generate_code.knowledge_updater import code_gen_mode,list_skills,view_error_log,auto_fix_plugins
import time
import json

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

def Function_cmd(cmd):
    # Split compound commands
    commands = split_compound_commands(cmd.lower())
    
    # Code Generation
    if any(trigger in cmd for trigger in [
        'generate code for', 'create a script for', 'make a python script for',
        'build a program for', 'develop code for', 'write code for',
        'generate plugin for', 'create plugin for', 'make plugin for',
        'code generation for', 'create a python script'
    ]):
        try:
            prompt = cmd
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
                return False
                
            print(f"Generating code for: {prompt}")
            print(f"\n[⚡ Generating Code For]: {prompt}")
            code_gen_mode(prompt, execute=True)
            print("\n[🔍 Running Post-Generation Checks]")
            list_skills()
            view_error_log()
            auto_fix_plugins()
            print("Code generation process completed")
            return True
            
        except Exception as e:
            error_msg = f"Error during code generation: {str(e)}"
            print(error_msg)
            print(error_msg)
            return False

    # LinkedIn Posting
    elif any(trigger in cmd for trigger in [
        'do the linkedin post', 'linkedin post', 'post on linkedin',
        'post in linkedin', 'share on linkedin', 'publish to linkedin',
        'create linkedin post', 'make linkedin post', 'post to linkedin now'
    ]):
        try:
            print("Preparing LinkedIn post...")
            success = main_linkedin()
            
            if success:
                print("Successfully posted on LinkedIn")
                print("LinkedIn post completed successfully")
                return True
            else:
                print("Could not complete the LinkedIn post")
                print("LinkedIn post failed")
                return False
                
        except Exception as e:
            error_msg = f"Error while posting to LinkedIn: {str(e)}"
            print(error_msg)
            print(error_msg)
            return False

    # Blog Posting
    elif any(trigger in cmd for trigger in [
        'post data science blog', 'post data scientist blog', 'publish data science article',
        'post data analysis blog', 'post data analyst blog', 'publish data analysis article',
        'post web development blog', 'post website development blog', 'publish web dev article',
        'post digital marketing blog', 'publish marketing article', 'post digital marketing post',
        'post graphic design blog', 'publish design article', 'post graphics blog',
        'post statistical analysis blog', 'post statistical blog', 'publish stats article',
        'post market research blog', 'publish research article', 'post market research post',
        'post market analysis blog', 'post market analyst blog', 'publish market analysis'
    ]):
        params = {'status': 'publish', 'index': 0, 'website': False}
        
        if 'as draft' in cmd:
            params['status'] = 'draft'
        elif 'as private' in cmd:
            params['status'] = 'private'
            
        params['website'] = 'in website' in cmd
        
        # Determine category
        if any(trigger in cmd for trigger in ['post data science blog', 'post data scientist blog', 'publish data science article']):
            category = 'data_science'
        elif any(trigger in cmd for trigger in ['post data analysis blog', 'post data analyst blog', 'publish data analysis article']):
            category = 'data_analysis'
        elif any(trigger in cmd for trigger in ['post web development blog', 'post website development blog', 'publish web dev article']):
            category = 'web_development'
        elif any(trigger in cmd for trigger in ['post digital marketing blog', 'publish marketing article', 'post digital marketing post']):
            category = 'digital_marketing'
        elif any(trigger in cmd for trigger in ['post graphic design blog', 'publish design article', 'post graphics blog']):
            category = 'graphic_design'
        elif any(trigger in cmd for trigger in ['post statistical analysis blog', 'post statistical blog', 'publish stats article']):
            category = 'statistical_analysis'
        elif any(trigger in cmd for trigger in ['post market research blog', 'publish research article', 'post market research post']):
            category = 'market_research'
        elif any(trigger in cmd for trigger in ['post market analysis blog', 'post market analyst blog', 'publish market analysis']):
            category = 'market_analysis'
            
        post_category_blog(category=category, post_index=params['index'], status=params['status'])
        return True

    # Email Extraction
    elif any(trigger in cmd for trigger in [
        'extract emails', 'scrape emails', 'get emails',
        'extract the mails', 'find email addresses', 'collect emails',
        'harvest emails', 'save mails', 'save all email',
        'save emails', 'store emails'
    ]):
        params = {'immediate': False, 'limit': None, 'domain': None}
        
        if 'now' in cmd or 'immediately' in cmd:
            params['immediate'] = True
            
        if 'first' in cmd:
            params['limit'] = 1
        elif 'top' in cmd:
            try:
                params['limit'] = int(cmd.split('top')[1].split()[0])
            except (IndexError, ValueError):
                params['limit'] = 10
                
        domain_keywords = ['from', 'for', 'at']
        for keyword in domain_keywords:
            if keyword in cmd:
                parts = cmd.split(keyword)
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
            
        extract_emails_from_websites(**call_params)
        return True

    # Content Storage
    elif any(trigger in cmd for trigger in [
        'store blog for website', 'save blog for website', 'store article for website',
        'save content for website', 'archive post for website'
    ]):
        params = {'immediate': False, 'review': False}
        
        if 'now' in cmd or 'immediately' in cmd:
            params['immediate'] = True
        if 'review' in cmd or 'check first' in cmd:
            params['review'] = True
            
        call_params = {
            'chat_log_path': r"D:\python\jervis\Data\ChatLog.json",
            'output_dir': r"D:\python\jervis\Data"
        }
        
        if params['review']:
            call_params['review'] = True
        if params['immediate']:
            call_params['immediate'] = True
            
        analyze_and_store_content_for_website(**call_params)
        return True
        
    elif any(trigger in cmd for trigger in [
        'store the article for linkedin', 'save this blog for linkedin',
        'save the article for linkedin', 'store this article for linkedin',
        'archive post for linkedin', 'save for linkedin'
    ]):
        params = {'immediate': False, 'review': False}
        
        if 'now' in cmd or 'immediately' in cmd:
            params['immediate'] = True
        if 'review' in cmd or 'check first' in cmd:
            params['review'] = True
            
        call_params = {
            'chat_log_path': r"D:\python\jervis\Data\ChatLog.json",
            'output_file_path': r"D:\python\jervis\Data\LinkedInPosts.json"
        }
        
        if params['review']:
            call_params['review'] = True
        if params['immediate']:
            call_params['immediate'] = True
            
        analyze_and_store_for_linkedin(**call_params)
        return True

    # Browser and System Controls
    elif any(trigger in cmd for trigger in ['visit', 'launch', 'open website']):
        webbrowser.open(f"https://www.{cmd.split()[-1]}.com")
        print(f"Visiting {cmd.split()[-1]}")
        return True
        
    elif any(trigger in cmd for trigger in ['play', 'pause', 'stop']):
        gui.hotkey("space")
        print("Media control executed")
        return True
        
    elif any(trigger in cmd for trigger in ['maximize window', 'maximize this']):
        gui.hotkey("win", "up")
        print("Maximizing window")
        return True
        
    elif any(trigger in cmd for trigger in ['minimise window', 'minimise this', 'minimize it']):
        gui.hotkey("win", "up")
        print("Maximizing window")
        return True
        
    elif 'restore window' in cmd:
        gui.hotkey("win", "shift", "up")
        print("Restoring window")
        return True
        
    elif any(trigger in cmd for trigger in ['switch window', 'next window']):
        gui.hotkey("alt", "tab")
        print("Switching to next window")
        return True
        
    elif any(trigger in cmd for trigger in ['previous window', 'back window']):
        gui.hotkey("alt", "shift", "tab")
        print("Switching to previous window")
        return True
        
    elif any(trigger in cmd for trigger in ['open incognito', 'private window']):
        gui.hotkey("ctrl", "shift", "n")
        print("Opening incognito window")
        return True
        
    elif any(trigger in cmd for trigger in ['bookmark page', 'save page']):
        gui.hotkey("ctrl", "d")
        print("Bookmarking page")
        return True
        
    elif any(trigger in cmd for trigger in ['shutdown', 'turn off computer']):
        gui.hotkey("win","d")
        time.sleep(0.4)
        gui.hotkey("alt", "f4")
        time.sleep(0.4)
        gui.press("enter")
        print("Shutting down")
        return True

    # Text Editing
    elif any(trigger in cmd for trigger in ['write', 'type']):
        print("writing boss")
        gui.write(cmd.replace("write", "").replace("type", "").strip())
        print("Text written")
        return True
        
    elif any(trigger in cmd for trigger in ['enter', 'press enter']):
        gui.press("enter")
        print("Enter pressed")
        return True
        
    elif any(trigger in cmd for trigger in ['select all', 'select all this']):
        print("done boss")
        gui.hotkey("ctrl", "a")
        print("All content selected")
        return True
        
    elif any(trigger in cmd for trigger in ['copy', 'copy this']):
        gui.hotkey("ctrl", "c")
        print("Content copied")
        return True
        
    elif any(trigger in cmd for trigger in ['paste', 'paste here']):
        gui.hotkey("ctrl", "v")
        print("Content pasted")
        return True
        
    elif any(trigger in cmd for trigger in ['undo', 'undo karo', 'back', 'back karo']):
        gui.hotkey("ctrl", "z")
        print("Action undone")
        return True
        
    elif any(trigger in cmd for trigger in ['cut', 'cut this']):
        gui.hotkey("ctrl", "x")
        print("Content cut")
        return True
        
    elif any(trigger in cmd for trigger in ['redo', 'redo karo', 'forward', 'forward karo']):
        gui.hotkey("ctrl", "y")
        print("Action redone")
        return True
        
    elif any(trigger in cmd for trigger in ['delete', 'delete this']):
        gui.press("delete")
        print("Content deleted")
        return True
        
    elif any(trigger in cmd for trigger in ['backspace', 'remove']):
        gui.press("backspace")
        print("Character removed")
        return True

    # Time
    elif "what is the time" in cmd or "time" in cmd or "what time is" in cmd:
        what_is_the_time()
        return True

    # IP Address
    elif "find my ip" in cmd or "ip address" in cmd:
        print("your ip is " + find_ip())
        return True

    # If no command matched
    else:
        return False