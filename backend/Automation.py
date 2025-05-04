from AppOpener import close, open as appopen
from webbrowser import open as webopen
from pywhatkit import search, playonyt
from bs4 import BeautifulSoup
from rich import print
from groq import Groq
import subprocess
import requests
import keyboard
import asyncio
import os
import webbrowser


# Load environment variables
GroqAPIKey = "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"

# Initialize Groq client
client = Groq(api_key=GroqAPIKey)

# Common response templates
professional_responses = [
    "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
    "I'm at your service for any additional questions or support you may need—don't hesitate to ask."
]

# List to store chatbot messages
messages = []

# System instruction for chatbot
SystemChatBot = [{
    "role": "system",
    "content": f"Hello, I am {os.environ.get('USERNAME', 'AI Assistant')}. You're a content writer. You have to write content like letters, codes, applications, essays, notes, songs, poems, etc."
}]

# Function to search on Google
def GoogleSearch(topic):
    search(topic)
    return True

# Function to generate content
def Content(topic):
    def OpenNotepad(file):
        subprocess.Popen(['notepad.exe', file])
    
    def ContentWriterAI(prompt):
        messages.append({"role": "user", "content": prompt})
        completion = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=SystemChatBot + messages,
            max_tokens=2048,
            temperature=0.7,
            top_p=1
        )
        Answer = completion.choices[0].message["content"].strip()
        messages.append({"role": "assistant", "content": Answer})
        return Answer
    
    topic = topic.replace("Content", "").strip()
    content_by_ai = ContentWriterAI(topic)
    file_path = rf"Data\{topic.lower().replace(' ', '_')}.txt"
    
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content_by_ai)
    
    OpenNotepad(file_path)
    return True

# Function to search YouTube
def YouTubeSearch(topic):
    url = f"https://www.youtube.com/results?search_query={topic}"
    webbrowser.open(url)
    return True

# Function to play a video on YouTube
def PlayYoutube(query):
    playonyt(query)
    return True

# Function to open an application
def OpenApp(app):
    try:
        appopen(app, match_closest=True, output=True, throw_error=True)
        return True
    except:
        print(f"Failed to open {app}. Searching online...")
        url = f"https://www.google.com/search?q={app}+app+download"
        webopen(url)
        return False

# Function to close an application
def CloseApp(app):
    try:
        close(app, match_closest=True, output=True, throw_error=True)
        return True
    except:
        return False

# System control functions
def System(command):
    actions = {
        "mute": lambda: keyboard.press_and_release("volume mute"),
        "unmute": lambda: keyboard.press_and_release("volume mute"),
        "volume up": lambda: keyboard.press_and_release("volume up"),
        "volume down": lambda: keyboard.press_and_release("volume down")
    }
    if command in actions:
        actions[command]()
        return True
    return False

# Async function to process commands
async def TranslateAndExecute(commands: list[str]):
    tasks = []
    for command in commands:
        if command.startswith("open "):
            tasks.append(asyncio.to_thread(OpenApp, command.removeprefix("open app")))
        elif command.startswith("close "):
            tasks.append(asyncio.to_thread(CloseApp, command.removeprefix("close ")))
        elif command.startswith("play "):
            tasks.append(asyncio.to_thread(PlayYoutube, command.removeprefix("play ")))
        elif command.startswith("content "):
            tasks.append(asyncio.to_thread(Content, command.removeprefix("content ")))
        elif command.startswith("google search "):
            tasks.append(asyncio.to_thread(GoogleSearch, command.removeprefix("open ")))
        elif command.startswith("youtube search "):
            tasks.append(asyncio.to_thread(YouTubeSearch, command.removeprefix("youtube search ")))
        elif command.startswith("system "):
            tasks.append(asyncio.to_thread(System, command.removeprefix("system ")))
        else:
            print(f"No function found for: {command}")
    
    results = await asyncio.gather(*tasks)
    for result in results:
        yield result

# Async automation function
async def Automation(commands: list[str]):
    async for _ in TranslateAndExecute(commands):
        pass
    return True

# Main execution
#if __name__ == "__main__":
    asyncio.run(Automation(["open facebook", "open instagram", "play afsanay", "content song for me"]))
