import cohere
from rich import print  # Import the Rich library to enhance terminal outputs.

# Retrieve API key securely
CohereAPIKey = "GgMy8Rjg7j7MwIKBF6vEVQzyMNkw7I5rIxVl7rn0"

# Create a Cohere client using the provided API key.
co = cohere.Client(api_key=CohereAPIKey)

# Define a list of recognized function keywords for task categorization.
funcs = [
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
    "Create a Python script"
    "exit",
    "generate image",
    "general", "gysten",
    "realtime",
    "open",
    "close", "play",
    "content",
    "youtube search", "reminder",
    "google search",
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
    "are you there",
    "hello there",
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
    "its time to post in website about statistical analysis"
]

# Initialize an empty list to store user messages.
messages = []

# Define the preamble that guides the AI model on how to categorize queries.
preamble = """
You are a very accurate Decision-Making Model, which decides what kind of a query is given to you.
You will decide whether a query is a 'general' query, a 'realtime' query, or is asking to perform any task or automation like 'open facebook, instagram', 'can you write an application and open it in notepad.'
*** Do not answer any query, just decide what kind of query is given to you. ***

-> Respond with 'general (query)' if a query can be answered by a LLM model (conversational AI chatbot) and doesn't require up-to-date information.
-> Respond with 'realtime (query)' if a query requires up-to-date information.
-> Respond with 'open (application name)' if a query is asking to open an application.
-> Respond with 'close (application name)' if a query is asking to close an application.
-> Respond with 'play (song name)' if a query is asking to play a song.
-> Respond with 'generate image (image prompt)' if a query requests an image generation.
-> Respond with 'reminder (datetime with message)' if a query requests a reminder.
-> Respond with 'system (task name)' for system-related tasks.
-> Respond with 'content (topic)' if a query is asking for content creation.
-> Respond with 'google search (topic)' if a query is requesting a Google search.
-> Respond with 'youtube search (topic)' if a query is requesting a YouTube search.
-> Respond with 'exit' if the user wants to end the conversation.

*** If a query is unclear, respond with 'general (query)' ***
"""

ChatHistory = [
    {"role": "User", "message": "how are you?"},
    {"role": "Chatbot", "message": "general how are you?"},
    {"role": "User", "message": "do you like pizza?"},
    {"role": "Chatbot", "message": "general do you like pizza?"},
    {"role": "User", "message": "open chrome and tell me about Mahatma Gandhi."},
    {"role": "Chatbot", "message": "open chrome, general tell me about Mahatma Gandhi."},
    {"role": "User", "message": "open chrome and firefox"},
    {"role": "Chatbot", "message": "open chrome, open firefox"},
    {"role": "User", "message": "what is today's date and remind me about my dance performance"},
    {"role": "Chatbot", "message": "general what is today's date, reminder 11:00pm 5th Aug dancing performance"},
    {"role": "User", "message": "chat with me."},
    {"role": "Chatbot", "message": "general chat with me."}
]

def FirstLayerDMM(prompt: str = "test"):
    """Processes user input and categorizes the query."""
    messages.append({"role": "user", "content": f"{prompt}"})

    # Cohere API call
    stream = co.chat_stream(
        model="command-r-plus",
        message=prompt,
        temperature=0.7,
        chat_history=ChatHistory,
        prompt_truncation="OFF",
        connectors=[],
        preamble=preamble
    )

    response = ""

    for event in stream:
        if event.event_type == "text-generation":
            response += event.text

    response = response.replace("\n", "").split(",")
    response = [i.strip() for i in response]

    # Validate response against predefined function keywords
    temp = [task for task in response if any(task.startswith(func) for func in funcs)]
    
    # Prevent infinite recursion
    if "(query)" in response:
        return "general " + prompt
    else:
        return temp

if __name__ == "__main__":
    while True:
        user_input = input(">>> ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Goodbye!")
            break
        print(FirstLayerDMM(user_input))
