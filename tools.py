import webbrowser
import urllib.parse

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