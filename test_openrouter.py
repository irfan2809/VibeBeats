import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Use the OPENROUTER_API_KEY environment variable if set
api_key = os.getenv("OPENROUTER_API_KEY")

def test_openrouter():
    """Test OpenRouter API functionality"""
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:5000",
        "X-Title": "Mood-to-Music Recommender"
    }
    
    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": "Say 'Hello, OpenRouter is working!'"}
        ],
        "max_tokens": 50
    }
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ OpenRouter API working!")
            print(f"Response: {data['choices'][0]['message']['content']}")
            return True
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing OpenRouter API")
    print("=" * 40)
    
    if not api_key:
        print("⚠️  Please set the OPENROUTER_API_KEY environment variable.")
        print("\n📝 To get a free API key:")
        print("1. Go to https://openrouter.ai/")
        print("2. Sign up for free")
        print("3. Get your API key from the dashboard")
        print("4. Set it in your environment: $env:OPENROUTER_API_KEY='your_key_here'")
    else:
        test_openrouter() 