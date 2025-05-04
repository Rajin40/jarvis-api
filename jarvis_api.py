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

def process_query(query, chat_history):
    """Cloud-friendly version without voice dependencies"""
    try:
        # Your existing processing logic but remove voice-specific parts
        decisions = FirstLayerDMM(query)
        
        if decisions:
            responses = []
            for decision in decisions:
                base_command = decision.split()[0] if decision else ""
                
                if base_command in ["google", "youtube"]:
                    responses.append(f"I would perform the search: {decision} (Note: Browser actions disabled in cloud mode)")
                
                elif decision.startswith("realtime"):
                    realtime_query = decision[9:] if decision.startswith("realtime") else query
                    responses.append(RealtimeSearchEngine(realtime_query))
                    
                else:
                    general_query = decision.split(" ", 1)[1] if " " in decision else query
                    responses.append(ChatBot(general_query))
            
            response = ". ".join(responses) if responses else "I'm not sure how to respond to that."
        else:
            response = ChatBot(query)
            
        return {"response": response}
        
    except Exception as e:
        return {"error": str(e)}

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
