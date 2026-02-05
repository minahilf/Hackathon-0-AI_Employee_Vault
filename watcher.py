import os
import shutil
import time


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INBOX = os.path.join(BASE_DIR, "Inbox")
NEEDS_ACTION = os.path.join(BASE_DIR, "Needs_Action")

print(f"👀 Watcher started")
print(f"Monitoring: {INBOX}")

def check_inbox():
    
    if os.path.exists(INBOX):
        files = os.listdir(INBOX)
        
        for file_name in files:
            
            if file_name.startswith("."):
                continue
                
            source = os.path.join(INBOX, file_name)
            destination = os.path.join(NEEDS_ACTION, file_name)
            
            
            try:
                shutil.move(source, destination)
                print(f"Moved: {file_name} -> Needs_Action folder")
            except Exception as e:
                print(f"Error moving {file_name}: {e}")

while True:
    check_inbox()
    time.sleep(2) 