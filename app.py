from flask import Flask, request, jsonify
from flask_cors import CORS
import asyncio
import json
import os
import datetime
import sys
import logging
from typing import Dict, List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import all your existing JARVIS components
sys.path.append("D:/python/jervis")
from backend.test import FirstLayerDMM
from backend.RealtimeSearchEngine import RealtimeSearchEngine
from Chrome_Intregretion.function_intregation import Function_cmd
from backend.chatbot import ChatBot

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
CHAT_LOG_PATH = r"Data\chatbot_data\ChatLog.json"
USERNAME = "boss"
ASSISTANT_NAME = "JARVIS"

class ChatManager:
    """Centralized chat management class"""
    
    def __init__(self):
        self.dmm = FirstLayerDMM()
        self._ensure_chat_log()
        
    def _ensure_chat_log(self) -> None:
        """Ensure chat log exists and is valid"""
        if not os.path.exists(CHAT_LOG_PATH):
            self.reset_chat_history()
        else:
            try:
                with open(CHAT_LOG_PATH, 'r', encoding='utf-8') as f:
                    json.load(f)
            except (json.JSONDecodeError, UnicodeDecodeError):
                logger.warning("Chat log corrupted - resetting...")
                self.reset_chat_history()
    
    def reset_chat_history(self) -> None:
        """Create a fresh chat history file"""
        try:
            os.makedirs(os.path.dirname(CHAT_LOG_PATH), exist_ok=True)
            with open(CHAT_LOG_PATH, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=4)
        except Exception as e:
            logger.error(f"Failed to reset chat history: {e}")
            raise

    def load_chat_history(self) -> List[Dict]:
        """Load chat history with robust error handling"""
        try:
            with open(CHAT_LOG_PATH, 'r', encoding='utf-8') as f:
                history = json.load(f)
                
                # Convert old format to new if needed
                if history and isinstance(history, list) and len(history) > 0 and "role" in history[0]:
                    logger.info("Converting old chat format to new format...")
                    new_history = [
                        {
                            "question": history[i]["content"],
                            "answer": history[i+1]["content"],
                            "timestamp": datetime.datetime.now().isoformat()
                        } 
                        for i in range(0, len(history), 2) 
                        if i+1 < len(history) and history[i]["role"] == "user"
                    ]
                    self.save_chat_history(new_history)
                    return new_history
                return history
        except (FileNotFoundError, json.JSONDecodeError, UnicodeDecodeError) as e:
            logger.warning(f"Error loading chat history: {e}")
            self.reset_chat_history()
            return []

    def save_chat_history(self, history: List[Dict]) -> None:
        """Save chat history with UTF-8 encoding"""
        try:
            with open(CHAT_LOG_PATH, 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=4)
        except Exception as e:
            logger.error(f"Error saving chat history: {e}")
            raise

    def check_existing_response(self, query: str, chat_history: List[Dict]) -> Optional[str]:
        """Check for existing response in chat history"""
        query_lower = query.lower()
        for entry in reversed(chat_history):
            if entry.get("question", "").lower() == query_lower:
                return entry.get("answer")
        return None

    async def process_query(self, query: str) -> Dict:
        """Process user query and return formatted response"""
        chat_history = self.load_chat_history()
        
        # Check for existing response first
        if existing_response := self.check_existing_response(query, chat_history):
            return {
                "response": existing_response,
                "from_memory": True
            }

        try:
            # Get DMM decision
            decision = self.dmm.categorize_query(query)
            cmd_type, *payload = decision.split(' ', 1)
            payload = payload[0] if payload else ""

            # Process based on command type
            if cmd_type == "exit":
                response = "exit"
            elif cmd_type in ["open", "close", "play", "system", "browser"]:
                success = Function_cmd(decision)
                response = f"Executed: {decision}" if success else f"Failed: {decision}"
            elif cmd_type == "realtime":
                if "ip" in payload.lower():
                    response = RealtimeSearchEngine("my IP address")
                elif "temperature" in payload.lower():
                    response = RealtimeSearchEngine("current temperature")
                elif "speed" in payload.lower():
                    response = RealtimeSearchEngine("internet speed test")
                else:
                    response = RealtimeSearchEngine(payload)
            elif cmd_type in ["google_search", "youtube_search"]:
                response = RealtimeSearchEngine(payload)
            elif cmd_type in ["content", "code_generation", "email"]:
                response = ChatBot(query)
            elif cmd_type == "reminder":
                response = f"Reminder set: {payload}"
            elif cmd_type == "ecommerce":
                response = f"Order placed: {payload}"
            else:
                response = ChatBot(query)

            # Update chat history
            chat_history.append({
                "question": query,
                "answer": response,
                "timestamp": datetime.datetime.now().isoformat()
            })
            self.save_chat_history(chat_history)

            return {
                "response": response,
                "from_memory": False
            }

        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return {
                "response": f"Sorry, I encountered an error: {str(e)}",
                "error": True
            }

# Initialize chat manager
chat_manager = ChatManager()

# API Endpoints
@app.route('/api/chat', methods=['POST'])
async def chat():
    """Handle chat requests"""
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"error": "Message is required"}), 400
        
        message = data['message'].strip()
        if not message:
            return jsonify({"error": "Message cannot be empty"}), 400

        # Process the query
        result = await chat_manager.process_query(message)
        
        return jsonify({
            "response": result["response"],
            "from_memory": result.get("from_memory", False),
            "status": "success"
        })

    except Exception as e:
        logger.error(f"API error: {e}")
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    """Get chat history"""
    try:
        history = chat_manager.load_chat_history()
        return jsonify({
            "history": history[-10:],  # Last 10 messages
            "count": len(history),
            "status": "success"
        })
    except Exception as e:
        logger.error(f"History error: {e}")
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

@app.route('/api/reset', methods=['POST'])
def reset_history():
    """Reset chat history"""
    try:
        chat_manager.reset_chat_history()
        return jsonify({"status": "success"})
    except Exception as e:
        logger.error(f"Reset error: {e}")
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

@app.route('/api/status', methods=['GET'])
def status():
    """Check API status"""
    return jsonify({
        "status": "running",
        "assistant": ASSISTANT_NAME,
        "username": USERNAME,
        "timestamp": datetime.datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
