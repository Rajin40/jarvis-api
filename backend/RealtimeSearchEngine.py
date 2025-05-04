import requests
from bs4 import BeautifulSoup
from groq import Groq
from json import load, dump
import datetime
import os

Username = "Rajin"
Assistantname = "jarvis"
GroqAPIKey = "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"

client = Groq(api_key=GroqAPIKey)

System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which has real-time up-to-date information from the internet.
*** Provide Answers In a Professional Way, make sure to add full stops, commas, question marks, and use proper grammar.***
*** Just answer the question from the provided data in a professional way. ***"""

def GoogleSearch(query):
    headers = {"User-Agent": "Mozilla/5.0"}
    params = {"q": query}
    response = requests.get("https://html.duckduckgo.com/html/", params=params, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    results = soup.find_all("a", {"class": "result__a"}, limit=5)
    descriptions = soup.find_all("a", {"class": "result__snippet"}, limit=5)

    Answer = f"The search results for '{query}' are:\n[start]\n"
    for i in range(len(results)):
        title = results[i].get_text(strip=True)
        description = descriptions[i].get_text(strip=True) if i < len(descriptions) else "No description available."
        Answer += f"Title: {title}\nDescription: {description}\n\n"
    Answer += "[end]"
    return Answer

def AnswerModifier(Answer):
    lines = Answer.split('\n')
    return '\n'.join([line for line in lines if line.strip()])

def Information():
    now = datetime.datetime.now()
    return (
        "Use This Real-time Information if needed: \n"
        f"Day: {now.strftime('%A')}\n"
        f"Date: {now.strftime('%d')}\n"
        f"Month: {now.strftime('%B')}\n"
        f"Year: {now.strftime('%Y')}\n"
        f"Time: {now.strftime('%H')} hours, {now.strftime('%M')} minutes, {now.strftime('%S')} seconds.\n"
    )

def RealtimeSearchEngine(prompt):
    chat_log_path = "Data/ChatLog.json"

    system_messages = [
        {"role": "system", "content": System},
        {"role": "system", "content": GoogleSearch(prompt)},
        {"role": "system", "content": Information()},
        {"role": "user", "content": prompt}
    ]

    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=system_messages,
        temperature=0.7,
        max_tokens=2048,
        top_p=1,
        stream=True,
        stop=None
    )

    Answer = ""
    for chunk in completion:
        if chunk.choices[0].delta.content:
            Answer += chunk.choices[0].delta.content

    Answer = Answer.strip().replace("</S>", "")
    final_answer = AnswerModifier(Answer)

    # Load previous history
    if os.path.exists(chat_log_path):
        with open(chat_log_path, "r") as f:
            try:
                chat_history = load(f)
            except:
                chat_history = []
    else:
        chat_history = []

    # Append user and assistant messages
    chat_history.append({"role": "user", "content": prompt})
    chat_history.append({"role": "assistant", "content": final_answer})

    # Save updated history
    with open(chat_log_path, "w") as f:
        dump(chat_history, f, indent=4)

    return final_answer

# Main interaction loop
# if __name__ == "__main__":
#     while True:
#         query = input("Enter your query: ")
#         print(RealtimeSearchEngine(query))
