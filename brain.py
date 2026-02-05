import os
import time
import sys
from google import genai
from dotenv import load_dotenv

# --- CONFIGURATION ---
class Config:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    ENV_PATH = os.path.join(BASE_DIR, ".env")
    NEEDS_ACTION = os.path.join(BASE_DIR, "Needs_Action")
    DONE = os.path.join(BASE_DIR, "Done")
    # File extensions to ignore
    IGNORE_FILES = {'.DS_Store', 'Thumbs.db'}

# --- UTILS: TERMINAL UI ---
def log(message, type="info"):
    """Prints clean messages to the console."""
    icons = {"info": "ℹ️", "success": "✅", "error": "❌", "wait": "⏳", "ai": "🤖"}
    print(f"{icons.get(type, '🔹')} {message}")

# --- SYSTEM SETUP ---
def initialize_system():
    """Loads environment and validates API key."""
    # 1. Load Environment
    if os.path.exists(Config.ENV_PATH):
        load_dotenv(Config.ENV_PATH)
    else:
        log(".env file not found!", "error")
        sys.exit(1)

    # 2. Get Key
    api_key = os.getenv("MY_API_KEY")
    if not api_key:
        log("API Key missing in .env (Check MY_API_KEY)", "error")
        sys.exit(1)

    # 3. Create Directories if missing
    os.makedirs(Config.NEEDS_ACTION, exist_ok=True)
    os.makedirs(Config.DONE, exist_ok=True)

    return api_key

# --- AI ENGINE ---
def get_best_model(client):
    """Automatically finds the best available Gemini model."""
    print("\n🔍 Scanning for available models...")
    
    try:
        all_models = list(client.models.list())
        candidates = []

        # Filter for Gemini text models
        for m in all_models:
            if "gemini" in m.name and "vision" not in m.name:
                clean_name = m.name.replace("models/", "")
                candidates.append(clean_name)

        # Sort: Prioritize 'flash' models for speed
        candidates.sort(key=lambda x: "flash" not in x)

        # Test models
        for model_name in candidates:
            try:
                print(f"   Testing: {model_name}...", end=" ")
                client.models.generate_content(model=model_name, contents="Ping")
                print("OK! ⚡")
                return model_name
            except:
                print("Failed.")
                continue

    except Exception as e:
        log(f"Model scan failed: {e}", "error")
    
    # Fallback default
    return "gemini-1.5-flash"

# --- CORE LOGIC ---
def process_file(client, model, file_name):
    """Reads a file, sends to AI, and saves the response."""
    file_path = os.path.join(Config.NEEDS_ACTION, file_name)
    
    # 1. Check if file actually exists (Ghost file fix)
    if not os.path.exists(file_path):
        return

    log(f"Processing: {file_name}", "wait")

    try:
        # Read Content
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        if not content.strip():
            return

        # Generate AI Response
        response = client.models.generate_content(
            model=model, 
            contents=f"Task: {content}"
        )

        # Save Response
        output_file = os.path.join(Config.DONE, f"REPLY_{file_name}")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(response.text)

        log(f"Task Complete! Saved to Done/REPLY_{file_name}", "success")
        
        # Cleanup
        os.remove(file_path)

    except Exception as e:
        log(f"Failed to process {file_name}: {e}", "error")

# --- MAIN LOOP ---
def main():
    os.system('cls' if os.name == 'nt' else 'clear') # Clear screen
    print("╔════════════════════════════════════════╗")
    print("║      🤖 AI EMPLOYEE VAULT: ONLINE      ║")
    print("╚════════════════════════════════════════╝")

    # 1. Setup
    key = initialize_system()
    try:
        client = genai.Client(api_key=key)
        active_model = get_best_model(client)
        log(f"Engine Active: {active_model}", "ai")
    except Exception as e:
        log(f"Connection Failed: {e}", "error")
        sys.exit(1)

    log(f"Monitoring folder: {Config.NEEDS_ACTION} ...\n", "info")

    # 2. Watch Loop
    while True:
        try:
            files = os.listdir(Config.NEEDS_ACTION)
            
            for file_name in files:
                if file_name.startswith(".") or file_name in Config.IGNORE_FILES:
                    continue
                
                process_file(client, active_model, file_name)
            
            time.sleep(2) # CPU ko saans lene do

        except KeyboardInterrupt:
            print("\n👋 System shutting down. Goodbye!")
            sys.exit(0)
        except Exception as e:
            log(f"System Error: {e}", "error")
            time.sleep(5)

if __name__ == "__main__":
    main()