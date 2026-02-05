# Personal AI Employee (Bronze Tier) 🤖

This project is a local-first AI Employee that operates autonomously to manage files and tasks. Built using Python and Gemini AI, it serves as a "Digital FTE" (Full-Time Equivalent).

## 🏆 Tier Achieved: Bronze
- **Foundation Layer:** Functional Obsidian Vault structure.
- **Perception:** Watcher script monitors `/Needs_Action` folder.
- **Reasoning:** Google Gemini 2.5 Flash processes tasks.
- **Action:** Autonomously writes results to `/Done` folder.

## 🛠️ Tech Stack
- **Language:** Python 3.12
- **AI Model:** Google Gemini 2.5 Flash
- **Interface:** File System (Obsidian Vault)

## 🚀 How to Run
1. Clone the repository.
2. Install dependencies: `pip install google-genai python-dotenv`
3. Add your API Key in `.env`.
4. Run the brain: `python brain.py`
5. Drop any task file into the `Needs_Action` folder to see the magic!

## 🔒 Security
- API Keys are stored in a `.env` file (not shared).
- Runs locally on the user's machine.