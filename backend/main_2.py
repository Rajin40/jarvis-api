import sys
sys.path.append("D:/python/jervis")
from threading import Thread
import schedule
from backend.auto_tasks import run_schedule
import asyncio
import json
import os
from backend.decisson_making_brain_model import FirstLayerDMM
from backend.RealtimeSearchEngine import RealtimeSearchEngine
from Chrome_Intregretion.function_intregation import Function_cmd
from backend.chatbot import ChatBot
from backend.talk_chatbot import talkChatBot
import datetime

# Configuration
CHAT_LOG_PATH = r"Data\chatbot_data\ChatLog.json"
USERNAME = "Rajin"
ASSISTANT_NAME = "JARVIS"

def reset_chat_history():
    """Create a fresh chat history file"""
    os.makedirs(os.path.dirname(CHAT_LOG_PATH), exist_ok=True)
    with open(CHAT_LOG_PATH, 'w', encoding='utf-8') as f:
        json.dump([], f, ensure_ascii=False, indent=4)

def load_chat_history():
    """Load chat history with robust error handling"""
    try:
        # Try reading with different encodings
        for encoding in ['utf-8', 'latin-1', 'utf-16']:
            try:
                with open(CHAT_LOG_PATH, 'r', encoding=encoding) as f:
                    history = json.load(f)
                    # Convert old format to new if needed
                    if history and isinstance(history, list) and len(history) > 0 and "role" in history[0]:
                        print("Converting old chat format to new format...")
                        new_history = []
                        for i in range(0, len(history), 2):
                            if i+1 < len(history) and history[i]["role"] == "user":
                                new_history.append({
                                    "question": history[i]["content"],
                                    "answer": history[i+1]["content"],
                                    "timestamp": str(datetime.datetime.now() - datetime.timedelta(minutes=len(history)-i))
                                })
                        save_chat_history(new_history)
                        return new_history
                    return history
            except UnicodeDecodeError:
                continue
            except json.JSONDecodeError:
                print("Chat log contains invalid JSON - resetting...")
                reset_chat_history()
                return []
        
        # If all encodings failed, reset the file
        print("Could not read chat log with any encoding - resetting...")
        reset_chat_history()
        return []
    except FileNotFoundError:
        reset_chat_history()
        return []

def save_chat_history(history):
    """Save chat history with UTF-8 encoding"""
    try:
        with open(CHAT_LOG_PATH, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error saving chat history: {e}")
        reset_chat_history()

def check_existing_response(query, chat_history):
    """Check for existing response in chat history"""
    for entry in reversed(chat_history):
        if entry.get("question", "").lower() == query.lower():
            return entry.get("answer")
    return None

async def process_query(query, chat_history):
    """Process user query using DMM and route based on decision"""
    query_lower = query.lower()
    
    # First check if this is an exact repeat question
    existing_response = check_existing_response(query, chat_history)
    if existing_response:
        print(f"[{ASSISTANT_NAME}] (from memory): {existing_response}")
        print(existing_response)
        return existing_response

    # Define command phrases (truncated for brevity - use your full list)
    COMMAND_PHRASES = {
    "action_commands": [
        "open", "close", "play", "content", "google ", "search",
        "check internet speed",
        "check speed test",
        "speed test",
        "check temperature",
        "temperature",
        "temprature",
        "temprature outside",
        "find my ip",
        "ip address",
        "what is my ip",
        "check my ip",
        "give me my ip",
        "tell me my ip",
        "what is the time",
        "time",
        "what time is",
        "wagt kya hai",
        "samay kya hai",
        "kitne baje hain",
        "kitna samay hua",
        "tell the time",
        "what time is now",
        "tell me the time",
        "youtube search", "system", "check", "find", "visit", 
        "launch", "search", "mute", "volume", "enter", "select",
        "copy", "paste", "undo", "scroll", "reload", "go back",
        "go forward", "stop", "maximize", "restore", "switch",
        "previous", "bookmark", "history", "downloads", "inspect",
        "clear", "fullscreen", "dark mode", "extensions", "settings",
        "save", "print", "new tab", "reopen", "show desktop",
        "virtual desktop", "notification", "action center",
        "lock screen", "log off", "shutdown", "restart", "sleep",
        "file explorer", "control panel", "navigate", "zoom",
        "search for", "start the work", "import gamil", "send mail",
        "send gmail", "send email", "send the mail", "send the email",
        "extract emails", "jervis you should do the linkedin post",
        "store the article", "store this article", "save the article", 
        "save this article", "kholo", "show me", "minimise", "minimize",
        "type", "press enter", "select all", "copy this",
        "paste here", "undo karo", "back karo", "copy last paragraph",
        "increase volume", "volume badhao", "increase sound", "decrease volume",
        "volume kam karo", "decrease sound", "full volume", "full volume kr do",
        "mute this", "mute tab", "unmute", "unmute tab", "open browser settings",
        "browser settings", "save page as", "save as", "print page", "print",
        "clear browsing data", "clear history", "open bookmarks", "view bookmarks",
        "reload page", "refresh it", "go back", "back", "go forward", "forward",
        "stop loading", "stop", "scroll up", "scroll page up", "scroll down",
        "scroll page down", "scroll to top", "scroll to bottom", "open new tab",
        "new tab", "reopen closed tab", "restore closed tab", "navigate forward",
        "forward jao", "zoom in on the current page", "current page me zoom",
        "zoom out on the current page", "zoom out", "start clap with music system",
        "start smart music system","post data science blog in website",
        "post data science blog",
        "post data scientist blog",
        "post data analysis blog in website",
        "post data analysis blog",
        "post data analyst blog",
        "post web development blog in website",
        "post web development blog",
        "post website development blog",
        "post digital marketing blog in website",
        "post digital marketing blog",
        "post graphic design blog in website",
        "post graphic design blog",
        "post statistical analysis blog in website",
        "post statistical analysis blog",
        "post statistical blog",
        "post market research blog in website",
        "post market research blog",
        "post market analysis blog in website",
        "post market analysis blog",
        "post market analyst blog","store article for website","save blog for website","store blog for website",
        "write", "generate",
        "its time to post in website about data analysis",
        "its time to post in website about data science",
        "its time to post in website about web development",
        "its time to post in website about graphic design",
        "its time to post in website about market analysis",
        "its time to post in website about market research",
        "its time to post in website about digital marketing",
        "its time to post in website about statistical analysis",
        "generate code for",
        "create a script for",
        "make a python script for",
        "build a program for",
        "develop code for",
        "write code for",
        "generate plugin for",
        "create plugin for",
        "make plugin for",
        "code generation for",
        "create a python script"
        
        
    ],
    "search_phrases": [
        "who is", "what is", "do you know", "can you find", "i need",
        "i want", "how to", "what was", "who was", "real time data",
        "give me real time data", "give me real time information", 
        "where is", "define", "teach me", "research"
    ],
    "chat_phrases": [
        "generate articel", "write articel","generate contect","make articel","make contect","write contect"
    ],
    "exit_commands": [
        "exit", "quit", "bye"
    ]
    }
    
    # Initialize default response
    response = "I'm not sure how to respond to that."
    
    try:
        # Use DMM to categorize the query
        decisions = FirstLayerDMM(query)
        if decisions:  # If DMM returned valid decisions
            responses = []
            action_commands = []
            
            for decision in decisions:
                if any(phrase in query_lower for phrase in COMMAND_PHRASES["action_commands"]):
                    Function_cmd(decision)
                    responses.append(f"I've executed the command: {decision}")
                elif any(phrase in query_lower for phrase in COMMAND_PHRASES["chat_phrases"]):
                    responses.append(ChatBot(decision))
                elif decision.startswith(("google", "youtube")):
                    Function_cmd(decision)
                    responses.append(f"I've performed the search: {decision}")
                elif decision.startswith("realtime") or any(phrase in query_lower for phrase in COMMAND_PHRASES["search_phrases"]):
                    realtime_query = decision[9:] if decision.startswith("realtime") else query
                    responses.append(RealtimeSearchEngine(realtime_query))
                elif decision == "exit":
                    return "exit"
                else:
                    general_query = decision.split(" ", 1)[1] if " " in decision else query
                    responses.append(talkChatBot(general_query))
            
            response = ". ".join(responses) if responses else response
        
        else:  # Fallback to phrase groups if DMM returns nothing
            if any(phrase in query_lower for phrase in COMMAND_PHRASES["action_commands"]):
                Function_cmd(query)
                response = f"I've executed the command: {query}"
            elif any(phrase in query_lower for phrase in COMMAND_PHRASES["search_phrases"]):
                response = RealtimeSearchEngine(query)
            elif any(phrase in query_lower for phrase in COMMAND_PHRASES["chat_phrases"]):
                response = ChatBot(query)
            elif query_lower in COMMAND_PHRASES["exit_commands"]:
                return "exit"
            else:
                response = talkChatBot(query)
                
        # Update chat history
        chat_history.append({
            "question": query,
            "answer": response,
            "timestamp": str(datetime.datetime.now())
        })
        save_chat_history(chat_history)
        
        return response
        
    except Exception as e:
        print(f"\n[{ASSISTANT_NAME}]: Sorry, I encountered an error: {str(e)}")
        print("Sorry, I encountered an error. Please try again.")
        return None

async def text_interaction_loop():
    """Main loop for text-based interaction"""
    chat_history = load_chat_history()
    
    print(f"\n{ASSISTANT_NAME} Assistant (Text Mode)")
    print("Type 'exit', 'quit', or 'bye' to end the session.\n")
    
    while True:
        try:
            user_input = input(f"[{USERNAME}]: ").strip()
            if not user_input:
                continue
                
            if user_input.lower() in ["exit", "quit", "bye"]:
                print(f"[{ASSISTANT_NAME}]: Goodbye!")
                print("Goodbye!")
                break
                
            response = await process_query(user_input, chat_history)
            if response == "exit":
                break
            elif response:
                print(f"[{ASSISTANT_NAME}]: {response}")
                print(response)
                
        except KeyboardInterrupt:
            print(f"\n[{ASSISTANT_NAME}]: Session ended by user.")
            break
        except Exception as e:
            print(f"\n[{ASSISTANT_NAME}]: Sorry, I encountered an error: {str(e)}")
            print("Sorry, I encountered an error. Please try again.")

def main():
    """Main entry point for the JARVIS assistant"""
    # Initialize chat log
    if not os.path.exists(CHAT_LOG_PATH):
        reset_chat_history()
    else:
        try:
            # Validate the existing file
            with open(CHAT_LOG_PATH, 'r', encoding='utf-8') as f:
                json.load(f)
        except:
            print("Existing chat log is corrupted - resetting...")
            reset_chat_history()

    print(f"\n{'='*50}")
    print(f"{ASSISTANT_NAME} Personal Assistant")
    print(f"{'='*50}\n")
    
    print("Choose interaction mode:")
    print("1. Text Mode")
    print("2. Voice Mode")
    print("3. Exit")
    
    while True:
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == "1":
            asyncio.run(text_interaction_loop())
            break
        elif choice == "2":
            print("Voice mode not implemented yet")
            break
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

# Start scheduler in background
Thread(target=run_schedule).start()

if __name__ == "__main__":
    main()