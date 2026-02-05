import os
import time
import sys
import datetime 
import json 
from google import genai
from dotenv import load_dotenv
from tools import post_to_linkedin, speak

# --- CONFIGURATION ---
class Config:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    ENV_PATH = os.path.join(BASE_DIR, ".env")
    NEEDS_ACTION = os.path.join(BASE_DIR, "Needs_Action")
    DONE = os.path.join(BASE_DIR, "Done")
    IGNORE_FILES = {'.DS_Store', 'Thumbs.db'}

# --- UTILS ---
def log(message, type="info"):
    icons = {"info": "ℹ️", "success": "✅", "error": "❌", "wait": "⏳", "ai": "🤖", "time": "⏰"}
    print(f"{icons.get(type, '🔹')} {message}")

def load_memory():
    """Memory file se user ka data nikalne ke liye"""
    memory_path = os.path.join(os.path.dirname(__file__), "memory.json")
    if os.path.exists(memory_path):
        with open(memory_path, "r") as f:
            return json.load(f)
    return {"user_name": "Minahil"} # Default agar file na mile

# --- SYSTEM SETUP ---
def initialize_system():
    if os.path.exists(Config.ENV_PATH):
        load_dotenv(Config.ENV_PATH)
    else:
        log(".env file not found!", "error")
        sys.exit(1)

    api_key = os.getenv("MY_API_KEY")
    if not api_key:
        log("API Key missing! Check .env file.", "error")
        sys.exit(1)

    os.makedirs(Config.NEEDS_ACTION, exist_ok=True)
    os.makedirs(Config.DONE, exist_ok=True)
    return api_key

# --- AI ENGINE (AUTO-FIXER) ---
def get_best_model(client):
    """Automatically finds the best available Gemini model."""
    print("\n🔍 Scanning for available models...")
    try:
        all_models = list(client.models.list())
        candidates = [m.name.replace("models/", "") for m in all_models if "gemini" in m.name and "vision" not in m.name]
        candidates.sort(key=lambda x: "flash" not in x)
        
        for model_name in candidates:
            try:
                print(f"   Testing: {model_name}...", end=" ")
                client.models.generate_content(model=model_name, contents="Ping")
                print("OK! ⚡")
                return model_name 
            except:
                continue
    except:
        pass
    return "gemini-1.5-flash"

# --- CORE LOGIC ---
def process_file(client, model, file_name):
    file_path = os.path.join(Config.NEEDS_ACTION, file_name)
    if not os.path.exists(file_path): return

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        if not content.strip(): return
        log(f"Processing: {file_name}", "wait")

        # Decide Persona
        if file_name.startswith("POST_"):
            system_instruction = "You are a LinkedIn Ghostwriter. Write a viral post under 100 words. Output ONLY the post body."
        elif file_name.startswith("AUTO_"):
            system_instruction = "You are a motivational coach. Give a 1-line quote."
        else:
            system_instruction = "You are Vault, Minahil's AI Employee. Be professional."

        # Generate Answer
        full_prompt = f"{system_instruction}\n\nTask: {content}"
        response = client.models.generate_content(model=model, contents=full_prompt)
        generated_text = response.text

        # Save Reply
        output_file = os.path.join(Config.DONE, f"REPLY_{file_name}")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(generated_text)
        
        # Gold Tier Voice Feedback
        log(f"Speaking status for {file_name}...", "ai")
        speak(f"Task {file_name} completed. I have saved the response.")

        # Execute Browser Action
        if file_name.startswith("POST_"):
            log("Opening Browser to Post...", "ai")
            post_to_linkedin(generated_text)
        
        os.remove(file_path)
        log(f"Task Finished: {file_name}", "success")

    except Exception as e:
        log(f"Error processing {file_name}: {e}", "error")

# --- MAIN LOOP ---
def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("╔════════════════════════════════════════╗")
    print("║      🥇 AI EMPLOYEE VAULT: ONLINE      ║")
    print("║       (Gold Tier: Voice & Memory)      ║")
    print("╚════════════════════════════════════════╝")

    key = initialize_system()
    client = genai.Client(api_key=key)

    active_model = get_best_model(client)
    log(f"Engine Active: {active_model}\n", "ai")
    
    # 👇 FIX: Memory load karke personalized greeting
    mem = load_memory()
    user = mem.get("user_name", "Minahil")
    speak(f"Welcome back {user}. Vault is online and ready.")

    log(f"Monitoring: {Config.NEEDS_ACTION}", "info")

    last_check_time = datetime.datetime.now()
    SCHEDULER_INTERVAL = 60 

    while True:
        try:
            files = os.listdir(Config.NEEDS_ACTION)
            for file_name in files:
                if file_name.startswith(".") or file_name in Config.IGNORE_FILES: continue
                process_file(client, active_model, file_name)
            
            current_time = datetime.datetime.now()
            if (current_time - last_check_time).seconds > SCHEDULER_INTERVAL:
                log("Scheduled Task Triggered", "time")
                task_file = os.path.join(Config.NEEDS_ACTION, f"AUTO_Briefing_{int(time.time())}.txt")
                with open(task_file, "w") as f:
                    f.write("Give a motivational line.")
                last_check_time = current_time 

            time.sleep(2) 

        except KeyboardInterrupt:
            speak("Vault is shutting down. Goodbye.")
            sys.exit(0)
        except Exception as e:
            log(f"System Error: {e}", "error")
            time.sleep(5)

if __name__ == "__main__":
    main()