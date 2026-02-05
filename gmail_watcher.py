import imaplib
import email
import os
import time
from email.header import decode_header
from dotenv import load_dotenv

# Config
load_dotenv()
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
NEEDS_ACTION = os.path.join(os.path.dirname(__file__), "Needs_Action")

def check_email():
    try:
        # Connect to Gmail
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(EMAIL_USER, EMAIL_PASS)
        mail.select("inbox")

        # Search Unread Emails
        status, messages = mail.search(None, '(UNSEEN)')
        email_ids = messages[0].split()

        if email_ids:
            print(f"📨 Processing {len(email_ids)} new emails...")
            
            for e_id in email_ids:
                res, msg_data = mail.fetch(e_id, "(RFC822)")
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        
                        # Subject Logic
                        subject, encoding = decode_header(msg["Subject"])[0]
                        if isinstance(subject, bytes):
                            subject = subject.decode(encoding if encoding else "utf-8")
                        
                        sender = msg.get("From")
                        print(f"🔹 Found: {subject} from {sender}")

                        # FILTER: Sirf 'Task' wali emails uthao
                        if "Task" in subject or "Urgent" in subject:
                            filename = f"EMAIL_Task_{int(time.time())}.txt"
                            with open(os.path.join(NEEDS_ACTION, filename), "w", encoding="utf-8") as f:
                                f.write(f"Email Task from {sender}:\n{subject}")
                            print("✅ Sent to AI Brain!")

        mail.close()
        mail.logout()

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("👀 Gmail Watcher Active (Waiting for emails with 'Task' in subject)...")
    while True:
        check_email()
        time.sleep(10)