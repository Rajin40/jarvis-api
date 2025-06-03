from typing import List, Union
import cohere
from rich import print
from dataclasses import dataclass

# Configuration class for better organization
@dataclass
class Config:
    COHERE_API_KEY = "GgMy8Rjg7j7MwIKBF6vEVQzyMNkw7I5rIxVl7rn0"
    MODEL_NAME = "command-r-plus"
    TEMPERATURE = 0.7

# Initialize Cohere client
co = cohere.Client(api_key=Config.COHERE_API_KEY)

# Define recognized function categories with type hints
FUNCTION_CATEGORIES = {
    "general": "queries answerable by LLM without real-time info",
    "realtime": "queries requiring up-to-date information",
    "open": "open an application",
    "close": "close an application",
    "play": "play a song",
    "generate image": "generate an image from prompt",
    "reminder": "set a reminder with datetime and message",
    "system": "system-related tasks",
    "content": "content creation requests",
    "google search": "Google search requests",
    "youtube search": "YouTube search requests",
    "exit": "end the conversation"
}

# Enhanced preamble with clearer instructions
PREAMBLE = """
You are an advanced Decision-Making Model that accurately categorizes user queries.
Your task is to determine whether a query is 'general', 'realtime', or a specific action request.

*** IMPORTANT RULES ***
1. NEVER answer the query directly - only categorize it
2. For multi-part queries, separate categories with commas
3. Be precise in identifying action requests
4. When in doubt, default to 'general'

CATEGORY FORMATS:
-> general (query): For conversational/LLM-answerable queries
-> realtime (query): For queries needing current information
-> open (app_name): Requests to open applications
-> close (app_name): Requests to close applications
-> play (song_name): Music playback requests
-> generate image (description): Image generation requests
-> reminder (datetime + message): Reminder creation
-> system (task): System-related operations
-> content (topic): Content creation requests
-> google search (query): Web search requests
-> youtube search (query): Video search requests
-> exit: Conversation termination

EXAMPLES:
User: "How's the weather?"
Response: "realtime weather"

User: "Open Chrome and tell me about AI"
Response: "open Chrome, general tell me about AI"

User: "Play Bohemian Rhapsody and set a reminder"
Response: "play Bohemian Rhapsody, reminder 5pm Meeting"
"""

# Enhanced chat history with more diverse examples
CHAT_HISTORY = [
    {"role": "User", "message": "how are you?"},
    {"role": "Chatbot", "message": "general how are you?"},
    {"role": "User", "message": "current stock price of Apple?"},
    {"role": "Chatbot", "message": "realtime current stock price of Apple"},
    {"role": "User", "message": "open notepad and write a poem"},
    {"role": "Chatbot", "message": "open notepad, content write a poem"},
    {"role": "User", "message": "search for AI news on Google"},
    {"role": "Chatbot", "message": "google search AI news"},
    {"role": "User", "message": "play jazz music and close Chrome"},
    {"role": "Chatbot", "message": "play jazz music, close Chrome"},
    {"role": "User", "message": "what's ChatGPT and show me tutorials"},
    {"role": "Chatbot", "message": "general what's ChatGPT, youtube search ChatGPT tutorials"}
]

class DecisionMakingModel:
    def __init__(self):
        self.messages = []
        
    def _validate_response(self, response: str) -> List[str]:
        """Validate and clean the model response"""
        response = response.replace("\n", "").strip()
        tasks = [task.strip() for task in response.split(",") if task.strip()]
        
        # Validate against known categories
        validated_tasks = []
        for task in tasks:
            # Check if task matches any known category prefix
            for category in FUNCTION_CATEGORIES:
                if task.startswith(category):
                    validated_tasks.append(task)
                    break
            else:
                # Default to general if no category matched
                validated_tasks.append(f"general {task}")
                
        return validated_tasks

    def categorize_query(self, prompt: str) -> Union[List[str], str]:
        """Categorize user input into appropriate action categories"""
        try:
            # Cohere API call with streaming
            stream = co.chat_stream(
                model=Config.MODEL_NAME,
                message=prompt,
                temperature=Config.TEMPERATURE,
                chat_history=CHAT_HISTORY,
                prompt_truncation="OFF",
                connectors=[],
                preamble=PREAMBLE
            )
            
            # Process streamed response
            response = "".join(
                event.text for event in stream 
                if event.event_type == "text-generation"
            )
            
            return self._validate_response(response)
            
        except Exception as e:
            print(f"[red]Error in categorization: {e}[/red]")
            return [f"general {prompt}"]

if __name__ == "__main__":
    dmm = DecisionMakingModel()
    
    print("[bold green]Decision Making Model v2.0[/bold green]")
    print("[italic]Type 'exit' to quit[/italic]")
    
    while True:
        try:
            user_input = input("\n>>> ").strip()
            if user_input.lower() in ["exit", "quit", "bye"]:
                print("Goodbye!")
                break
                
            if not user_input:
                continue
                
            result = dmm.categorize_query(user_input)
            print("[bold cyan]Categorized as:[/bold cyan]", result)
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break