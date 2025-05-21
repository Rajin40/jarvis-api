import sys
sys.path.append("D:/python/jervis")
import imaplib
import email
from plyer import notification
import pyttsx3
import time
import re
from backend.british_brian_Voice import speak
# Email Credentials
EMAIL = "rajinshale44@gmail.com"
PASSWORD = "fpaa kthn vyea uztc"  # Gmail App Password (enable 2FA)
IMAP_SERVER = "imap.gmail.com"

def extract_sender_and_message(email_body):
    # Extract sender name (common Fiverr patterns)
    sender = "Unknown Sender"
    sender_patterns = [
        r"from (\w+)",                      # "from username"
        r"messages? from (\w+)",             # "message from username"
        r"(\w+) sent you a message",         # "username sent you a message"
        r"Conversation with (\w+)",          # "Conversation with username"
        r"(\w+) has messaged you",           # "username has messaged you"
        r"New message from (\w+)"            # "New message from username"
    ]
    
    for pattern in sender_patterns:
        match = re.search(pattern, email_body, re.IGNORECASE)
        if match:
            sender = match.group(1)
            break
    
    # Extract message content (look for message after common markers)
    message = "No message content"
    message_patterns = [
        r'(?:Hi\b.*?[\r\n]+)(.*?)(?:\s*Go to your inbox|$)',  # After "Hi..."
        r'(?:wrote:[\r\n]+)(.*?)(?:\s*Reply|$)',              # After "wrote:"
        r'(?:message:[\r\n]+)(.*?)(?:\s*View conversation|$)', # After "message:"
        r'(?:said:[\r\n]+)(.*?)(?:\s*Respond|$)'              # After "said:"
    ]
    
    for pattern in message_patterns:
        match = re.search(pattern, email_body, re.DOTALL)
        if match:
            message = match.group(1).strip()
            # Clean up extra whitespace and newlines
            message = ' '.join(message.split())
            break
    
    return sender, message

def check_fiverr_emails():
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL, PASSWORD)
        mail.select("inbox")

        search_query = '(FROM "noreply@e.fiverr.com" SUBJECT "message")'
        result, data = mail.search(None, search_query)
        
        if result == "OK":
            email_ids = data[0].split()
            
            if not email_ids:
                speak("No new Fiverr messages found")
                mail.logout()
                return
                
            for num in email_ids:
                try:
                    result, msg_data = mail.fetch(num, "(RFC822)")
                    raw_email = msg_data[0][1]
                    msg = email.message_from_bytes(raw_email)
                    
                    email_body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                email_body = part.get_payload(decode=True).decode(errors='ignore')
                                break
                    else:
                        email_body = msg.get_payload(decode=True).decode(errors='ignore')
                    
                    # Print the raw email body for debugging
                    print("=" * 50)
                    print(email_body)
                    print("=" * 50)
                    
                    sender, message = extract_sender_and_message(email_body)
                    
                    notification.notify(
                        title=f"New Fiverr Message from {sender}",
                        message=f"{message[:100]}...",
                        timeout=10
                    )
                    speak(f"New Fiverr message from {sender}. Message: {message}")
                
                except Exception as e:
                    print(f"Error processing email: {e}")
                    continue

        mail.logout()
    except Exception as e:
        print(f"Error checking email: {e}")
        speak("Sorry, I encountered an error checking Fiverr messages")

# Run every 5 minutes
while True:
    check_fiverr_emails()
    time.sleep(300)