from flask import Flask, request, jsonify
import json
import os
# Instead of this:
# from backend.decisson_making_brain_model import FirstLayerDMM

# Use this:
from .backend.decisson_making_brain_model import FirstLayerDMM
from backend.RealtimeSearchEngine import RealtimeSearchEngine
from backend.Chatbot import ChatBot

app = Flask(__name__)

# Configuration
CHAT_LOG_PATH = "Data/ChatLog.json"  # Changed to forward slashes for cross-platform
USERNAME = "Rajin"
ASSISTANT_NAME = "JARVIS"

# ... [keep your existing load_chat_history, save_chat_history, check_existing_response functions] ...

# At the top with other imports
try:
    from backend.decisson_making_brain_model import FirstLayerDMM
    DMM_AVAILABLE = True
except ImportError as e:
    DMM_AVAILABLE = False
    print(f"Warning: Decision making module not available - {str(e)}")

# ... [keep other imports and config] ...

def process_query(query, chat_history):
    """Process user query with fallback when DMM is not available"""
    query_lower = query.lower()
    
    # First check if this is an exact repeat question
    existing_response = check_existing_response(query, chat_history)
    if existing_response:
        return {"response": existing_response, "from_memory": True}

    try:
        # Use DMM if available, otherwise use fallback
        decisions = FirstLayerDMM(query) if DMM_AVAILABLE else None
        
        if decisions:
            responses = []
            for decision in decisions:
                # ... [rest of your existing decision processing logic] ...
        else:
            # Fallback processing when DMM is not available
            if any(phrase in query_lower for phrase in COMMAND_PHRASES["action_commands"]):
                response = f"I would execute: {query} (Note: Actions disabled in cloud mode)"
            elif any(phrase in query_lower for phrase in COMMAND_PHRASES["search_phrases"]):
                response = RealtimeSearchEngine(query)
            else:
                response = ChatBot(query)
                
    except Exception as e:
        error_msg = f"Sorry, I encountered an error: {str(e)}"
        return {"error": error_msg}

    return {"response": response}

@app.route('/api/query', methods=['POST'])
def handle_query():
    data = request.json
    query = data.get('query', '').strip()
    
    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    chat_history = load_chat_history()
    result = process_query(query, chat_history)
    
    if 'error' not in result:
        chat_history.append({"role": "user", "content": query})
        chat_history.append({"role": "assistant", "content": result['response']})
        save_chat_history(chat_history)
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
