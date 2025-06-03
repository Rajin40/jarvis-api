import sys
sys.path.append("D:/python/jervis")
from json import load, dump
import datetime
from backend.confic import *
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from difflib import SequenceMatcher

Username = "Rajin"
Assistantname = "jarvis"

# Initialize the DialoGPT model
model_path = "D:/python/DialoGPT-medium"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path)

# Set pad token if not already set
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

# Initialize chat history
conversation_history = []

# Create chatbot_data directory if it doesn't exist
import os
os.makedirs(r"Data\chatbot_data", exist_ok=True)

# Load ResponseGuidance.json
try:
    with open(r"Data\chatbot_data\ResponseGuidance.json", "r") as f:
        response_guidance = load(f)
except FileNotFoundError:
    response_guidance = []
    with open(r"Data\chatbot_data\ResponseGuidance.json", "w") as f:
        dump(response_guidance, f, indent=4)

# Define the system prompt with guidance
System = f"""You are {Assistantname}, an AI assistant. Follow these guidelines:
- Be friendly and professional
- Keep answers concise
- Answer in English only
- Ask for clarification if needed
"""

def similar(a, b):
    """Check if two strings are similar using SequenceMatcher"""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio() > 0.8

def find_similar_question(current_question, chat_log):
    """Find similar questions in chat log"""
    for entry in reversed(chat_log):  # Check most recent first
        if similar(current_question, entry["question"]):
            return entry["answer"]
    return None

def talkChatBot(Query):
    """Send query to local AI model and save Q&A to log."""
    global conversation_history
    
    try:
        # First check if we have a similar question in ChatLog.json
        try:
            with open(r"Data\chatbot_data\ChatLog.json", "r") as f:
                chat_log = load(f)
                similar_answer = find_similar_question(Query, chat_log)
                if similar_answer:
                    # Add to conversation history
                    conversation_history.append(f"User: {Query}")
                    conversation_history.append(f"{Assistantname}: {similar_answer}")
                    return similar_answer
        except FileNotFoundError:
            chat_log = []

        # If no similar question found, generate new response
        # Add user message to history
        conversation_history.append(f"User: {Query}")
        
        # Prepare prompt with recent history (last 3 exchanges)
        recent_history = "\n".join(conversation_history[-6:])  # Keep last 3 exchanges
        prompt = f"{System}\n{recent_history}\n{Assistantname}:"
        
        # Tokenize with attention mask
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
        
        # Generate response
        outputs = model.generate(
            inputs.input_ids,
            attention_mask=inputs.attention_mask,
            max_new_tokens=150,
            pad_token_id=tokenizer.eos_token_id,
            temperature=0.7,
            top_p=0.9,
            do_sample=True
        )
        
        # Decode the response
        Answer = tokenizer.decode(outputs[0][inputs.input_ids.shape[-1]:], skip_special_tokens=True)
        
        # Clean up response
        Answer = Answer.split("\n")[0].strip()
        Answer = Answer.replace(Assistantname + ":", "").strip()
        
        # Add assistant response to history
        conversation_history.append(f"{Assistantname}: {Answer}")
        
        # Save to log
        chat_log.append({
            "question": Query,
            "answer": Answer,
            "timestamp": str(datetime.datetime.now())
        })
        
        with open(r"Data\chatbot_data\ChatLog.json", "w") as f:
            dump(chat_log, f, indent=4)

        return Answer

    except Exception as e:
        print(f"Error: {e}")
        return "Something went wrong. Please try again."

# if __name__ == "__main__":
#     print(f"🤖 {Assistantname} is ready! Type 'exit' to quit.\n")
#     while True:
#         user_input = input("You: ")
#         if user_input.lower() == 'exit':
#             break
#         response = talkChatBot(user_input)
#         print(f"{Assistantname}:", response)
#         print(response)