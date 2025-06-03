import os
import json
import hashlib
import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from threading import Thread
import time
import sys

# Add your custom module path
sys.path.append("D:/python/jervis")
from Chrome_Intregretion.function_intregation import Function_cmd
from backend.RealtimeSearchEngine import RealtimeSearchEngine
from backend.chatbot import ChatBot
#from backend.auto_tasks import run_all_jobs_every_30_seconds

# Configuration
CONFIG = {
    "CHAT_LOG_PATH": os.path.join("Data", "chatbot_data", "ChatLog.json"),  # Kept for reading only
    "SESSION_STORE": os.path.join("Data", "chatbot_data", "sessions"),
    "MAX_HISTORY": 50,
    "HISTORY_PRUNE_DAYS": 30,
    "DEFAULT_RESPONSE": "I'm here to help. What would you like to know?",
    "COMMAND_PHRASES": {
        "action_commands": ["open", "close", "play", "google", "search"],
        "search_phrases": ["who is", "do you know", "can you find","who was", "real time data",
                           "give me real time data", "give me real time information", "where is", "define", "teach me", "research"],
        "exit_commands": ["exghgjhfdfgfjdghujytyfghfvghfgh"]
    }
}

# Setup Flask
app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("JARVIS")

# Ensure directories exist
os.makedirs(CONFIG["SESSION_STORE"], exist_ok=True)

class ChatLogManager:
    @staticmethod
    def load_responses():
        """Load response data from chatlog (read-only)"""
        try:
            if os.path.exists(CONFIG["CHAT_LOG_PATH"]):
                with open(CONFIG["CHAT_LOG_PATH"], 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        return data
                    return []
            return []
        except Exception as e:
            logger.error(f"Failed to load response data: {e}")
            return []

    @staticmethod
    def find_response(query):
        """Find response with exact matching (read-only)"""
        try:
            query = query.lower().strip()
            for entry in ChatLogManager.load_responses():
                if isinstance(entry, dict) and entry.get("question", "").lower() == query:
                    return entry.get("answer")
            return None
        except Exception as e:
            logger.error(f"Error finding response: {e}")
            return None

class CommandHandler:
    @staticmethod
    def handle_command(query):
        """Process all command types"""
        query_lower = query.lower()
        
        # Check exit commands first
        if any(cmd in query_lower for cmd in CONFIG["COMMAND_PHRASES"]["exit_commands"]):
            return {
                "response": "Goodbye!",
                "type": "exit",
                "should_exit": True
            }
        
        # Handle action commands
        action_commands = []
        if any(cmd in query_lower for cmd in CONFIG["COMMAND_PHRASES"]["action_commands"]):
            action_commands = [cmd for cmd in CONFIG["COMMAND_PHRASES"]["action_commands"] 
                             if cmd in query_lower]
            try:
                result = Function_cmd(action_commands)
                return {
                    "response": f"Executing action: {', '.join(action_commands)}",
                    "type": "action",
                    "commands": action_commands
                }
            except Exception as e:
                logger.error(f"Action error: {e}")
                return {
                    "response": "I couldn't complete that action",
                    "type": "error"
                }
        
        # Handle search phrases
        if any(phrase in query_lower for phrase in CONFIG["COMMAND_PHRASES"]["search_phrases"]):
            search_term = query_lower
            for phrase in CONFIG["COMMAND_PHRASES"]["search_phrases"]:
                search_term = search_term.replace(phrase, "").strip()
            
            try:
                result = RealtimeSearchEngine(search_term)
                return {
                    "response": str(result),
                    "type": "search",
                    "source": "realtime"
                }
            except Exception as e:
                logger.error(f"Search error: {e}")
                return {
                    "response": "I couldn't complete that search",
                    "type": "error"
                }
        
        # # Handle chat phrases
        # if any(phrase in query_lower for phrase in CONFIG["COMMAND_PHRASES"]["chat_phrases"]):
        #     try:
        #         response = ChatBot(query)
        #         return {
        #             "response": str(response),
        #             "type": "chat"
        #         }
        #     except Exception as e:
        #         logger.error(f"ChatBot error: {e}")
        
        # return None

@app.route('/chat', methods=['POST'])
def handle_chat():
    """Main chat endpoint that checks chatlog first"""
    try:
        data = request.get_json()
        user_input = data.get('message', '').strip()
        session_id = data.get('session_id', 'default')
        
        if not user_input:
            return jsonify({"error": "Empty message"}), 400

        # 1. Check if this is a command
        command_response = CommandHandler.handle_command(user_input)
        if command_response:
            if command_response.get("should_exit"):
                return jsonify(command_response)
            return jsonify(command_response)

        # 2. Check ChatLog.json for matching response
        chatlog_response = ChatLogManager.find_response(user_input)
        if chatlog_response is not None:
            return jsonify({
                "response": chatlog_response,
                "type": "chat",
                "source": "chatlog"
            })

        # 3. Generate custom response if no match found
        generated_response = {
            "response": ChatBot(user_input),
            "type": "chat"
        }
        
        return jsonify(generated_response)
        
    except Exception as e:
        logger.error(f"Chat endpoint error: {e}")
        return jsonify({
            "response": "I encountered a system error. Please try again.",
            "type": "error"
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
