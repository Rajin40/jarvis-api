import sys
sys.path.append("D:/python/jervis")
from groq import Groq
from json import load, dump
import datetime
from backend.british_brian_Voice import speak
from backend.confic import *
import os

Username = "Rajin"
Assistantname = "jarvis"
GroqAPIKey = "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"

# Initialize the Groq client
client = Groq(api_key=GroqAPIKey)

# Initialize an empty list for user messages
messages = []

# Create chatbot_data directory if it doesn't exist
os.makedirs(r"Data\chatbot_data", exist_ok=True)

# Load ResponseGuidance.json
try:
    with open(r"Data\chatbot_data\ResponseGuidance.json", "r", encoding='utf-8') as f:
        response_guidance = load(f)
except FileNotFoundError:
    response_guidance = []
    with open(r"Data\chatbot_data\ResponseGuidance.json", "w", encoding='utf-8') as f:
        dump(response_guidance, f, indent=4)
except Exception as e:
    print(f"Error loading ResponseGuidance.json: {e}")
    response_guidance = []

# Create guidance string for system prompt
guidance_string = "Response Guidance:\n"
for category in response_guidance:
    guidance_string += f"Category: {category['category']}\n"
    guidance_string += f"Guidance: {category['guidance']}\n"
    guidance_string += "Examples:\n"
    for example in category['examples']:
        guidance_string += f"- Query: {example['query']}\n  Response: {example['response']}\n"
    guidance_string += "\n"

# Define the system prompt with guidance
System = f"""You are {Assistantname}, an advanced and accurate AI assistant created to provide concise, helpful, and reliable answers for {Username}. You have access to real-time internet information to ensure up-to-date responses. Follow these guidelines:
- Respond in a friendly and professional tone, keeping answers clear and concise.
- Answer only in English, regardless of the query's language.
- Do not provide the time or date unless explicitly requested.
- Use real-time data when relevant (e.g., for weather, news, or current events), and cite the context briefly if needed.
- If a query is unclear or incomplete, politely ask for clarification.
- Avoid including notes, explanations, or mentions of your training data unless requested.
- Ensure responses are culturally sensitive and appropriate for a global audience.
- If unable to answer due to limitations, say: 'I'm sorry, I can't assist with that. Please try rephrasing or ask something else.'
- Use the following guidance to shape your response style, adapting creatively to the query while maintaining the specified tone and structure:
{guidance_string}
"""

SystemChatBot = [{"role": "system", "content": System}]

# Load ChatLog.json
try:
    with open(r"Data\chatbot_data\ChatLog.json", "r", encoding='utf-8') as f:
        messages = load(f)
except FileNotFoundError:
    messages = []
    with open(r"Data\chatbot_data\ChatLog.json", "w", encoding='utf-8') as f:
        dump(messages, f, indent=4)
except Exception as e:
    print(f"Error loading ChatLog.json: {e}")
    messages = []

def RealtimeInformation():
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")

    data = (
        f"Please use this real-time information if needed:\n"
        f"Day: {day}\nDate: {date}\nMonth: {month}\nYear: {year}\n"
        f"Time: {hour} hours : {minute} minutes : {second} seconds.\n"
    )
    return data

def AnswerModifier(Answer):
    lines = Answer.split("\n")
    non_empty_lines = [line.strip() for line in lines if line.strip()]
    modified_answer = "\n".join(non_empty_lines)
    return modified_answer

def ChatBot(Query):
    """Send query to AI with guidance from ResponseGuidance.json and save Q&A to log."""
    try:
        # Prepare system + time + current user message
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
            with open(r"Data\chatbot_data\ChatLog.json", "r", encoding='utf-8') as f:
                log = load(f)
        except (FileNotFoundError, Exception) as e:
            print(f"Error loading chat log: {e}")
            log = []

        # Save in question-answer format
        qa_pair = {
            "question": Query,
            "answer": Answer,
            "timestamp": datetime.datetime.now().isoformat()
        }
        log.append(qa_pair)
        
        try:
            with open(r"Data\chatbot_data\ChatLog.json", "w", encoding='utf-8') as f:
                dump(log, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving chat log: {e}")

        return Answer

    except Exception as e:
        print(f"Error in ChatBot function: {e}")
        Answer = "Something went wrong. Please try again."
        
        try:
            with open(r"Data\chatbot_data\ChatLog.json", "r", encoding='utf-8') as f:
                log = load(f)
        except (FileNotFoundError, Exception) as e:
            print(f"Error loading chat log: {e}")
            log = []
        
        qa_pair = {
            "question": Query,
            "answer": Answer,
            "timestamp": datetime.datetime.now().isoformat()
        }
        log.append(qa_pair)
        
        try:
            with open(r"Data\chatbot_data\ChatLog.json", "w", encoding='utf-8') as f:
                dump(log, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving chat log: {e}")
        
        return Answer

if __name__ == "__main__":
    print(f"{Assistantname}: Hello {Username}, how can I assist you today?")
    speak(f"Hello {Username}, how can I assist you today?")
    
    while True:
        try:
            user_input = input(f"{Username}: ")
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print(f"{Assistantname}: Goodbye {Username}!")
                speak(f"Goodbye {Username}!")
                break
                
            response = ChatBot(user_input)
            print(f"{Assistantname}: {response}")
            speak(response)
        except KeyboardInterrupt:
            print(f"\n{Assistantname}: Goodbye {Username}!")
            speak(f"Goodbye {Username}!")
            break
        except Exception as e:
            print(f"{Assistantname}: Sorry, I encountered an error: {e}")
            speak("Sorry, I encountered an error. Please try again.")