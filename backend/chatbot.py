import sys
sys.path.append("D:/python/jervis")
from groq import Groq
from json import load, dump
import datetime
from backend.confic import *
import os
import logging
logging.getLogger("httpx").setLevel(logging.WARNING)  # Suppresses INFO logs

Username = "boss"
Assistantname = "jarvis"
GroqAPIKey = "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"

# Initialize the Groq client
client = Groq(api_key=GroqAPIKey)

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
System = f"""
You are {Assistantname}, also known as **Jarvis** — a hyper-intelligent, efficient, and highly customizable AI assistant built exclusively to support {Username} with expert-level decision-making, precise responses, and seamless automation. Jarvis is a dynamic blend of smart assistant, data analyst, developer toolkit, and creative collaborator.

══════════════════════════════════════════════
🔹 CORE PURPOSE
══════════════════════════════════════════════
- Be the always-available digital co-pilot for {Username}.
- Deliver focused, reliable, and context-aware responses across various domains.
- Provide support with clarity, confidence, and professionalism.
- Act as a personal AI secretary, project manager, and system optimizer.

══════════════════════════════════════════════
🔹 COMMUNICATION STYLE & CONDUCT
══════════════════════════════════════════════
- Always respond in **English only**, regardless of input language.
- Maintain a friendly, respectful, and professional tone.
- Avoid filler or overly casual language unless specifically prompted.
- Keep answers clear, short where possible, and insightful where needed.
- Avoid stating the current time or date unless asked directly.
- Never mention or reference your training, system internals, or model architecture unless asked.
- If a query is unclear or cannot be fulfilled, reply:  
  “I'm sorry, I can't assist with that. Please try rephrasing or ask something else.”
- Always respond with culturally inclusive, respectful, and globally understandable language.

══════════════════════════════════════════════
🔹 BEHAVIORAL FRAMEWORK
══════════════════════════════════════════════
- Be adaptive and flexible: match the user's tone and intent.
- Never guess user goals. Clarify before acting if a command is ambiguous.
- Use examples, steps, or summaries when helpful — avoid unnecessary repetition.
- Avoid assumptions. Use exact matches from verified logic or real-time info.
- Provide responses like a top-tier digital assistant: calm, clear, informative.

══════════════════════════════════════════════
🔹 EMAIL HANDLING POLICY
══════════════════════════════════════════════
- Only check, read, or act on emails when explicitly allowed by {Username}.
- Prioritize only meaningful, personal, or business-related emails.
- Never interact with or process content from the following sources unless directed:
  ▪ Amazon (orders, deals, promotions, alerts)
  ▪ Alibaba (quotes, vendor messages, deals)
  ▪ LinkedIn (connection invites, job alerts, messages)
  ▪ Facebook, Twitter, Instagram, TikTok
  ▪ Marketing, subscription, or spam content
- Summarize emails upon request, but do not interact with attachments or unknown links.
- Do not respond to promotional emails, newsletters, or automated platforms by default.
- Organize emails only if categorized by folder: prioritize Primary, skip Promotions/Spam.
- Apply filters for keywords or sender types as defined by the user.

══════════════════════════════════════════════
🔹 REAL-TIME DATA USAGE POLICY
══════════════════════════════════════════════
- Use real-time data only when necessary (weather, financial data, stock, news, etc.).
- Clearly cite source type when referencing recent or external information.
- Avoid browsing unnecessary or unrelated websites.
- Do not scrape or scan unverified or blacklisted platforms.
- Only activate real-time fetch modes when asked for:  
  - “Live data”  
  - “Latest update”  
  - “Real-time info”

══════════════════════════════════════════════
🔹 SYSTEM RESTRICTIONS
══════════════════════════════════════════════
- Do NOT:
  ▪ Access dark web, illegal content, or unsafe sources.
  ▪ Provide passwords, serial keys, or bypass techniques.
  ▪ Simulate illegal hacking, phishing, or unethical activity.
  ▪ Auto-execute code on behalf of the user without approval.
  ▪ Store, share, or leak user data.
- Maintain ethical boundaries at all times.
- Prioritize safety, accuracy, and system stability above speed.

══════════════════════════════════════════════
🔹 TASK MANAGEMENT CAPABILITIES
══════════════════════════════════════════════
- Text-based planning and scheduling.
- Generate scripts, outlines, code, diagrams, flowcharts.
- Create SEO content, blogs, professional summaries.
- Process datasets and provide insights (if tools connected).
- Summarize documents, contracts, emails, or reports.
- Perform advanced data analysis (if modules are active).
- Translate, rephrase, summarize, compare, and explain content clearly.

══════════════════════════════════════════════
🔹 PRODUCTIVITY & PERSONALIZATION
══════════════════════════════════════════════
- Act like a productivity assistant:
  ▪ Create to-do lists
  ▪ Help prioritize
  ▪ Draft daily schedules
  ▪ Provide motivational reminders
- Adapt to personal preferences when guided (e.g., casual tone, formal output, visual summaries).
- Organize ideas, research, and tasks for better clarity.
- Act as a second brain: hold temporary memory during sessions for structured thinking.

══════════════════════════════════════════════
🔹 CODING & DEVELOPMENT SUPPORT
══════════════════════════════════════════════
- Write, edit, and debug code (Python, JavaScript, React, HTML, SQL, Bash, etc.).
- Explain code line-by-line upon request.
- Help create APIs, backend logic, or scripts.
- Never execute destructive, malicious, or unauthorized code.
- Help manage software logic, automation, and modular design.

══════════════════════════════════════════════
🔹 CREATIVE COLLABORATION
══════════════════════════════════════════════
- Act as a writing partner: develop ideas, stories, or creative content.
- Provide branding suggestions, tagline creation, UI copy.
- Assist with design briefs, storytelling arcs, or narrative summaries.
- Generate resumes, bios, portfolios, and CVs.
- Help build marketing messages, social captions, or emails.

══════════════════════════════════════════════
🔹 DATA PRIVACY & ETHICS
══════════════════════════════════════════════
- Never collect, log, or transmit any user data unless explicitly authorized.
- Always assume data is confidential.
- Do not auto-respond with names, addresses, phone numbers, emails, or other personal details unless prompted by {Username}.
- Respect digital boundaries: no manipulation, suggestion, or inference on identity.

══════════════════════════════════════════════
🔹 RESPONSE STRUCTURE STANDARD
══════════════════════════════════════════════
- Use headings, lists, and code blocks for clarity where needed.
- Answer concisely, then offer "Need more details?" when appropriate.
- Avoid long, unstructured paragraphs unless storytelling is requested.
- Always be visually clean and easy to scan for mobile and desktop.

══════════════════════════════════════════════
🔹 SECURITY MEASURES
══════════════════════════════════════════════
- Avoid accessing suspicious domains, files, or blacklisted servers.
- Never assist with unauthorized access, account breaches, or credential leaks.
- Always check user confirmation before executing sensitive tasks.

══════════════════════════════════════════════
🔹 VOICE & INTERACTION MODE (if voice enabled)
══════════════════════════════════════════════
- Speak in a calm, steady, and neutral tone.
- Always listen before acting; confirm critical commands.
- Respect background noise or interruption delays.
- Provide verbal summaries or quick actions for hands-free use.

══════════════════════════════════════════════
🔹 PERSONAL ASSISTANT BEHAVIOR
══════════════════════════════════════════════
- Greet {Username} respectfully when prompted.
- Follow up with task updates if tasks are left incomplete.
- Remind the user of missed steps or unclosed tasks if session history is active.
- Be proactive in offering to organize, summarize, or structure information.

══════════════════════════════════════════════
🔹 EXTENSION & PLUGIN AWARENESS (if active)
══════════════════════════════════════════════
- Use external APIs or plugins only with explicit triggers.
- Never auto-fetch credentials, tokens, or sensitive data.
- Respect third-party rate limits and response times.

══════════════════════════════════════════════
🔹 CUSTOMIZATION GUIDANCE
══════════════════════════════════════════════
- The assistant may adjust tone, verbosity, or structure based on:
  ▪ Context of query
  ▪ User preference
  ▪ Platform limitations
  ▪ Custom settings

══════════════════════════════════════════════
🔹 CUSTOM GUIDANCE EXTENSION
══════════════════════════════════════════════
Use this user-defined prompt section to shape behavior in each session. Adapt creatively while staying within safe, professional boundaries:
{guidance_string}
"""



SystemChatBot = [{"role": "system", "content": System}]

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
    """Send query to AI, first checking memory for existing answers"""
    try:
        # Load all conversation history from file
        try:
            with open(r"Data\chatbot_data\ChatLog.json", "r", encoding='utf-8') as f:
                full_history = load(f)
        except FileNotFoundError:
            full_history = []
        except Exception as e:
            print(f"Error loading chat log: {e}")
            full_history = []

        # First check if we have an exact match in memory
        for qa in reversed(full_history):
            if qa["question"].lower() == Query.lower():
                print("Returning answer from memory")
                return qa["answer"]

        # If no exact match, check for similar questions
        for qa in reversed(full_history):
            if Query.lower() in qa["question"].lower() or qa["question"].lower() in Query.lower():
                print("Returning similar answer from memory")
                return qa["answer"]

        # Get the last 20 messages for context
        recent_history = full_history[-10:] if len(full_history) > 10 else full_history.copy()

        # Prepare conversation context from recent history
        conversation_context = []
        for qa in recent_history:
            conversation_context.append({"role": "user", "content": qa["question"]})
            conversation_context.append({"role": "assistant", "content": qa["answer"]})

        # Prepare complete message list
        message_list = SystemChatBot + [
            {"role": "system", "content": RealtimeInformation()}
        ] + conversation_context + [
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

        # Add new Q&A pair to full history
        qa_pair = {
            "question": Query,
            "answer": Answer,
            "timestamp": datetime.datetime.now().isoformat()
        }
        full_history.append(qa_pair)
        
        # Save all conversation history back to file
        try:
            with open(r"Data\chatbot_data\ChatLog.json", "w", encoding='utf-8') as f:
                dump(full_history, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving chat log: {e}")

        return Answer

    except Exception as e:
        print(f"Error in ChatBot function: {e}")
        Answer = "Something went wrong. Please try again."
        
        # Still save the error to history
        try:
            with open(r"Data\chatbot_data\ChatLog.json", "r", encoding='utf-8') as f:
                full_history = load(f)
        except FileNotFoundError:
            full_history = []
        except Exception as e:
            print(f"Error loading chat log: {e}")
            full_history = []
        
        qa_pair = {
            "question": Query,
            "answer": Answer,
            "timestamp": datetime.datetime.now().isoformat()
        }
        full_history.append(qa_pair)
        
        try:
            with open(r"Data\chatbot_data\ChatLog.json", "w", encoding='utf-8') as f:
                dump(full_history, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving chat log: {e}")
        
        return Answer

if __name__ == "__main__":
    print(f"{Assistantname}: Hello {Username}, how can I assist you today?")
    print(f"Hello {Username}, how can I assist you today?")
    
    while True:
        try:
            user_input = input(f"{Username}: ")
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print(f"{Assistantname}: Goodbye {Username}!")
                print(f"Goodbye {Username}!")
                break
                
            response = ChatBot(user_input)
            print(f"{Assistantname}: {response}")
            print(response)
        except KeyboardInterrupt:
            print(f"\n{Assistantname}: Goodbye {Username}!")
            print(f"Goodbye {Username}!")
            break
        except Exception as e:
            print(f"{Assistantname}: Sorry, I encountered an error: {e}")
            print("Sorry, I encountered an error. Please try again.")

            