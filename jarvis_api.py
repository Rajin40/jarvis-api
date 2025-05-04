from flask import Flask, request, jsonify
from concurrent.futures import ThreadPoolExecutor
import json
import os
from backend.decisson_making_brain_model import FirstLayerDMM
from backend.RealtimeSearchEngine import RealtimeSearchEngine
from Chrome_Intregretion.function_intregation import Function_cmd
from backend.British_Brian_Voice import speak
from backend.Chatbot import ChatBot
from backend.Voice import listen

app = Flask(__name__)
executor = ThreadPoolExecutor()

# Configuration
CHAT_LOG_PATH = r"Data\ChatLog.json"
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
    for i in range(len(chat_history) - 1, -1, -1):
        if chat_history[i].get("role") == "user" and chat_history[i].get("content", "").lower() == query.lower():
            if i + 1 < len(chat_history) and chat_history[i + 1].get("role") == "assistant":
                return chat_history[i + 1].get("content")
    return None

def process_query(query, chat_history):
    """Process user query using DMM and route based on decision"""
    query_lower = query.lower()
    
    # First check if this is an exact repeat question
    existing_response = check_existing_response(query, chat_history)
    if existing_response:
        return {"response": existing_response, "from_memory": True}

    # Your existing COMMAND_PHRASES dictionary here...
    COMMAND_PHRASES = {
        # ... (keep your existing command phrases)
    }

    # Initialize default response
    response = "I'm not sure how to respond to that."
    
    try:
        # Use DMM to categorize the query
        decisions = FirstLayerDMM(query)
        
        if decisions:  # If DMM returned valid decisions
            responses = []
            for decision in decisions:
                # Extract the base command (first word)
                base_command = decision.split()[0] if decision else ""
                
                if base_command in ["open", "close", "play", "system"]:
                    Function_cmd(decision)
                    responses.append(f"I've executed the command: {decision}")
                    
                elif base_command in ["google", "youtube"]:
                    Function_cmd(decision)
                    responses.append(f"I've performed the search: {decision}")
                    
                elif decision.startswith("realtime") or any(phrase in query_lower for phrase in COMMAND_PHRASES["search_phrases"]):
                    realtime_query = decision[9:] if decision.startswith("realtime") else query
                    responses.append(RealtimeSearchEngine(realtime_query))
                    
                elif decision == "exit":
                    return {"response": "exit", "exit": True}
                    
                else:
                    general_query = decision.split(" ", 1)[1] if " " in decision else query
                    responses.append(ChatBot(general_query))
            
            response = ". ".join(responses) if responses else response
        
        else:  # Fallback to phrase groups if DMM returns nothing
            if any(phrase in query_lower for phrase in COMMAND_PHRASES["action_commands"]):
                Function_cmd(query)
                response = f"I've executed the command: {query}"
            elif any(phrase in query_lower for phrase in COMMAND_PHRASES["search_phrases"]):
                response = RealtimeSearchEngine(query)
            elif query_lower in COMMAND_PHRASES["exit_commands"]:
                return {"response": "exit", "exit": True}
            else:
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
    mode = data.get('mode', 'text')  # 'text' or 'voice'
    
    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    chat_history = load_chat_history()
    result = process_query(query, chat_history)
    
    # Update chat history
    if 'error' not in result:
        chat_history.append({"role": "user", "content": query})
        chat_history.append({"role": "assistant", "content": result['response']})
        save_chat_history(chat_history)
    
    # Handle voice mode
    if mode == 'voice' and 'response' in result:
        speak(result['response'])
    
    return jsonify(result)

@app.route('/api/voice', methods=['GET'])
def voice_input():
    """Get voice input"""
    try:
        print("Listening...")
        user_input = listen()
        return jsonify({"input": user_input})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)