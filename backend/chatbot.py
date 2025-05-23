import sys
sys.path.append("D:/python/jervis")
from groq import Groq
from json import load, dump
import datetime
from backend.british_brian_Voice import speak  # Import the voice module
from backend.confic import *


Username = "Rajin"
Assistantname = "jarvis"
GrogAPIKey = GroqAPIKey

# Initialize the Groq client using the provided API key
client = Groq(api_key=GrogAPIKey)

# Initialize an empty list to store user messages
messages = []

# Define the preamble that guides the AI model
System = f"""Hello, I am {Username}. You are a very accurate and advanced AI chatbot named {Assistantname}, 
which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask. Do not talk too much, just answer the question. ***
*** Reply in only English, even if the question is in Hindi. ***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""

SystemChatBot = [{"role": "system", "content": System}]

# Attempt to load the chat log from a JSON file
try:
    with open(r"Data\ChatLog.json", "r") as f:
        messages = load(f)  # Load existing messages from the chat log
except FileNotFoundError:
    with open(r"Data\ChatLog.json", "w") as f:
        dump([], f)


def RealtimeInformation():
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")

    # Format the real-time information
    data = (
        f"Please use this real-time information if needed:\n"
        f"Day: {day}\nDate: {date}\nMonth: {month}\nYear: {year}\n"
        f"Time: {hour} hours : {minute} minutes : {second} seconds.\n"
    )
    return data


def AnswerModifier(Answer):
    lines = Answer.split("\n")  # Split the response into lines
    non_empty_lines = [line.strip() for line in lines if line.strip()]
    modified_answer = "\n".join(non_empty_lines)  # Join non-empty lines
    return modified_answer


# Main chatbot function to handle user queries
def ChatBot(Query):
    """Send only the latest query to the AI and save Q&A to log."""
    try:
        # Prepare system + time + current user message (no history)
        message_list = SystemChatBot + [
            {"role": "system", "content": RealtimeInformation()},
            {"role": "user", "content": Query}
        ]

        # Send request to AI
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=message_list,
            max_tokens=1024,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None,
        )

        Answer = ""
        for chunk in completion:
            if hasattr(chunk.choices[0].delta, "content") and chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content

        Answer = Answer.replace("</s>", "")
        Answer = AnswerModifier(Answer)

        # Load existing Q&A log
        try:
            with open(r"Data\ChatLog.json", "r") as f:
                log = load(f)
        except FileNotFoundError:
            log = []

        # Save new Q&A pair in the desired format
        qa_pair = {
            "question": Query,
            "answer": Answer
        }
        log.append(qa_pair)
        
        with open(r"Data\ChatLog.json", "w") as f:
            dump(log, f, indent=4)

        return Answer

    except Exception as e:
        print(f"Error: {e}")
        return "Something went wrong. Please try again."




if __name__ == "__main__":
     while True:
        user_input = input("Enter Your Question: ")
        speak(ChatBot(user_input))