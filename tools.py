import webbrowser
import urllib.parse
import pyttsx3

def speak(text):
    """AI ki awaaz nikalne wala function"""
    try:
        engine = pyttsx3.init()
        # Voice ki speed (150-200 best hai)
        engine.setProperty('rate', 170) 
        # Voice volume (0.0 to 1.0)
        engine.setProperty('volume', 1.0)
        
        print(f"🔊 AI Speaking: {text[:50]}...")
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"❌ Voice Error: {e}")

def post_to_linkedin(text):
    """
    Ye function browser khol kar LinkedIn par post draft karega.
    """
    print(f"🚀 Opening LinkedIn to post: {text[:30]}...")
    
    # Text ko URL format mein convert karo (Spaces ko %20 banata hai)
    encoded_text = urllib.parse.quote(text)
    
    # LinkedIn ka Share URL banao
    linkedin_url = f"https://www.linkedin.com/feed/?shareActive=true&text={encoded_text}"
    
    # Browser open karo
    webbrowser.open(linkedin_url)
    
    return "✅ Browser opened! Please click 'Post' to publish."

# Test karne ke liye (Run karke dekho)
if __name__ == "__main__":
    post_to_linkedin("Hello LinkedIn! This is a test from my AI Employee. 🤖 #AI #Python")