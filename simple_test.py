import requests
import json

# Use the API key directly
api_key = "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"

print(f"🔑 Testing API key: {api_key[:20]}...")

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    "HTTP-Referer": "http://localhost:5000",
    "X-Title": "Mood-to-Music Recommender"
}

payload = {
    "model": "openai/gpt-3.5-turbo",
    "messages": [
        {"role": "user", "content": "Say 'Hello, API is working!'"}
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
        print("✅ API working!")
        print(f"Response: {data['choices'][0]['message']['content']}")
    else:
        print(f"❌ API Error: {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"❌ Error: {e}") 