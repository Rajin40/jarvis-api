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

def extract_upwork_details(email_body):
    # Check if it's an interview invitation
    interview_match = re.search(r"Invitation to Interview for: (.+?)\n", email_body)
    if interview_match:
        job_title = interview_match.group(1).strip()
        
        # Extract client notes if available
        notes_match = re.search(r"Notes\n(.+?)\n\n", email_body, re.DOTALL)
        notes = notes_match.group(1).strip() if notes_match else "No additional notes"
        
        # Extract payment details
        payment_match = re.search(r"Estimated Time\s*\|\s*(.+?)\n", email_body)
        estimated_time = payment_match.group(1).strip() if payment_match else "Not specified"
        
        return {
            'type': 'interview',
            'job_title': job_title,
            'notes': notes,
            'estimated_time': estimated_time
        }
    
    # Check for regular messages
    message_match = re.search(r"Congrats! You have been invited(.+?)Submit Proposal", email_body, re.DOTALL)
    if message_match:
        sender_match = re.search(r"from (.+?) \(Upwork", email_body)
        sender = sender_match.group(1) if sender_match else "Unknown Client"
        
        message_content = message_match.group(1).strip()
        return {
            'type': 'message',
            'sender': sender,
            'content': message_content
        }
    
    return {'type': 'unknown'}

def check_upwork_emails():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL, PASSWORD)
    mail.select("inbox")

    # CORRECTED IMAP search syntax
    search_criteria = 'OR FROM "donotreply@upwork.com" FROM "notifications@upwork.com"'
    result, data = mail.search(None, search_criteria)  # Removed problematic parentheses
    
    if result == "OK":
        email_ids = data[0].split()
        
        if not email_ids:
            speak("No new Upwork notifications found")
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
                
                details = extract_upwork_details(email_body)
                
                if details['type'] == 'interview':
                    notification.notify(
                        title=f"Upwork Interview: {details['job_title']}",
                        message=f"Duration: {details['estimated_time']}",
                        timeout=15
                    )
                    speak(f"New interview for {details['job_title']}")
                    
                elif details['type'] == 'message':
                    notification.notify(
                        title=f"Upwork Message from {details['sender']}",
                        message=f"{details['content'][:100]}...",
                        timeout=10
                    )
                    speak(f"Message from {details['sender']}")

            except Exception as e:
                print(f"Error processing email: {str(e)}")
                continue

    mail.logout()

# Main loop (run every 5 minutes)
while True:
    check_upwork_emails()
    time.sleep(300)