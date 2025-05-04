from flask import Flask, request, jsonify
import json
import os
from concurrent.futures import ThreadPoolExecutor

# Import modules with error handling
try:
    from backend.decisson_making_brain_model import FirstLayerDMM
    DMM_AVAILABLE = True
except ImportError as e:
    DMM_AVAILABLE = False
    print(f"Warning: Decision making module not available - {str(e)}")

try:
    from backend.RealtimeSearchEngine import RealtimeSearchEngine
    SEARCH_AVAILABLE = True
except ImportError:
    SEARCH_AVAILABLE = False

try:
    from backend.Chatbot import ChatBot
    CHATBOT_AVAILABLE = True
except ImportError:
    CHATBOT_AVAILABLE = False

app = Flask(__name__)
executor = ThreadPoolExecutor()

# Configuration
CHAT_LOG_PATH = "Data/ChatLog.json"  # Using forward slashes for cross-platform
USERNAME = "Rajin"
ASSISTANT_NAME = "JARVIS"

def load_chat_history():
    """Load chat history from JSON file"""
    try:
        with open(CHAT_LOG_PATH, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_chat_history(history):
    """Save chat history to JSON file"""
    os.makedirs(os.path.dirname(CHAT_LOG_PATH), exist_ok=True)
    with open(CHAT_LOG_PATH, "w") as f:
        json.dump(history, f, indent=4)

def check_existing_response(query, chat_history):
    """Check if query exists in history"""
    for i in range(len(chat_history) - 1, -1, -1):
        if chat_history[i].get("role") == "user" and chat_history[i].get("content", "").lower() == query.lower():
            if i + 1 < len(chat_history) and chat_history[i + 1].get("role") == "assistant":
                return chat_history[i + 1].get("content")
    return None

COMMAND_PHRASES = {
    "action_commands": [
        "open", "close", "play", "content", "google search",
        "youtube search", "system", "check", "find", "visit", 
        "launch", "search", "mute", "volume", "enter", "select",
        # ... (keep your existing command phrases)
    ],
    "search_phrases": [
        "who is", "what is", "do you know", "can you find", "i need",
        "i want", "how to", "what was", "who was", "real time data",
        # ... (keep your existing search phrases)
    ],
    "exit_commands": ["exit", "quit", "bye"]
}

def process_query(query, chat_history):
    """Process user query with fallbacks for missing modules"""
    query_lower = query.lower()
    
    # Check for existing response
    existing_response = check_existing_response(query, chat_history)
    if existing_response:
        return {"response": existing_response, "from_memory": True}

    # Initialize response
    response = "I'm not sure how to respond to that."

    try:
        # Use DMM if available
        decisions = FirstLayerDMM(query) if DMM_AVAILABLE else None
        
        if decisions:
            responses = []
            for decision in decisions:
                base_command = decision.split()[0] if decision else ""
                
                if base_command in ["google", "youtube"]:
                    responses.append(f"I would perform the search: {decision} (Note: Browser actions disabled in cloud mode)")
                
                elif decision.startswith("realtime") and SEARCH_AVAILABLE:
                    realtime_query = decision[9:] if decision.startswith("realtime") else query
                    responses.append(RealtimeSearchEngine(realtime_query))
                    
                elif CHATBOT_AVAILABLE:
                    general_query = decision.split(" ", 1)[1] if " " in decision else query
                    responses.append(ChatBot(general_query))
            
            response = ". ".join(responses) if responses else response
        
        else:  # Fallback processing
            if any(phrase in query_lower for phrase in COMMAND_PHRASES["action_commands"]):
                response = f"I would execute: {query} (Note: Actions disabled in cloud mode)"
            elif any(phrase in query_lower for phrase in COMMAND_PHRASES["search_phrases"]) and SEARCH_AVAILABLE:
                response = RealtimeSearchEngine(query)
            elif CHATBOT_AVAILABLE:
                response = ChatBot(query)
                
    except Exception as e:
        error_msg = f"Sorry, I encountered an error: {str(e)}"
        return {"error": error_msg}

    return {"response": response}

@app.route('/api/query', methods=['POST'])
def handle_query():
    """Handle API queries"""
    data = request.json
    query = data.get('query', '').strip()
    
    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    chat_history = load_chat_history()
    result = process_query(query, chat_history)
    
    # Update chat history
    if 'error' not in result:
        chat_history.append({"role": "user", "content": query})
        chat_history.append({"role": "assistant", "content": result['response']})
        save_chat_history(chat_history)
    
    return jsonify(result)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "modules": {
        "decision_making": DMM_AVAILABLE,
        "search_engine": SEARCH_AVAILABLE,
        "chatbot": CHATBOT_AVAILABLE
    }})

if __name__ == '__main__':
    app.run(debug=True)
