from flask import Flask, request, jsonify
import json
import os
import datetime
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
    print("Warning: Search engine not available")

try:
    from backend.Chat_bot import ChatBot
    CHATBOT_AVAILABLE = True
except ImportError:
    CHATBOT_AVAILABLE = False
    print("Warning: Chatbot not available")

try:
    from backend.British_Brian_Voice import speak
    SPEECH_AVAILABLE = True
except ImportError:
    SPEECH_AVAILABLE = False
    print("Warning: Speech synthesis not available")

app = Flask(__name__)
executor = ThreadPoolExecutor()

# Configuration
CHAT_LOG_PATH = "Data/ChatLog.json"
USERNAME = "Rajin"
ASSISTANT_NAME = "JARVIS"

COMMAND_PHRASES = {
    "action_commands": [
        "open", "close", "play", "content", "google search",
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
        "search for", "start the work", "import gmail", "send mail",
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
        "post data science blog", "post data scientist blog",
        "post data analysis blog in website", "post data analysis blog",
        "post data analyst blog", "post web development blog in website",
        "post web development blog", "post website development blog",
        "post digital marketing blog in website", "post digital marketing blog",
        "post graphic design blog in website", "post graphic design blog",
        "post statistical analysis blog in website", "post statistical analysis blog",
        "post statistical blog", "post market research blog in website",
        "post market research blog", "post market analysis blog in website",
        "post market analysis blog", "post market analyst blog","store article for website",
        "save blog for website","store blog for website", "write", "generate",
        "its time to post in website about data analysis",
        "its time to post in website about data science",
        "its time to post in website about web development",
        "its time to post in website about graphic design",
        "its time to post in website about market analysis",
        "its time to post in website about market research",
        "its time to post in website about digital marketing",
        "its time to post in website about statistical analysis"
    ],
    "search_phrases": [
        "who is", "what is", "do you know", "can you find", "i need",
        "i want", "how to", "what was", "who was", "real time data",
        "give me real time data", "give me real time information", 
        "where is", "define", "teach me", "research"
    ],
    "exit_commands": ["exit", "quit", "bye"]
}

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
            elif query_lower in COMMAND_PHRASES["exit_commands"]:
                return {"response": "Goodbye!", "exit": True}
                
    except Exception as e:
        error_msg = f"Sorry, I encountered an error: {str(e)}"
        return {"error": error_msg}

    return {"response": response}

@app.route('/')
def home():
    """Root endpoint with API information"""
    return jsonify({
        "service": "Jarvis API",
        "status": "running",
        "version": "1.0",
        "endpoints": {
            "root": {"method": "GET", "description": "API information"},
            "health": {"method": "GET", "description": "Service health check"},
            "query": {"method": "POST", "description": "Process user queries"}
        },
        "modules": {
            "decision_making": DMM_AVAILABLE,
            "search_engine": SEARCH_AVAILABLE,
            "chatbot": CHATBOT_AVAILABLE,
            "speech_synthesis": SPEECH_AVAILABLE
        },
        "usage_example": {
            "method": "POST",
            "url": "/api/query",
            "headers": {"Content-Type": "application/json"},
            "body": {"query": "what time is it?"}
        },
        "documentation": "https://github.com/Rajin40/jarvis-api"
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "dependencies": {
            "decision_making": DMM_AVAILABLE,
            "search_engine": SEARCH_AVAILABLE,
            "chatbot": CHATBOT_AVAILABLE,
            "speech_synthesis": SPEECH_AVAILABLE
        },
        "system": {
            "python_version": os.sys.version,
            "platform": os.sys.platform
        }
    })

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

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "error": "Endpoint not found",
        "available_endpoints": {
            "root": {"method": "GET", "path": "/"},
            "health": {"method": "GET", "path": "/health"},
            "query": {"method": "POST", "path": "/api/query"}
        }
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        "error": "Internal server error",
        "message": str(error)
    }), 500

if __name__ == '__main__':
    app.run(debug=True)
