from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure OpenRouter API
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze_mood', methods=['POST'])
def analyze_mood():
    try:
        data = request.get_json()
        user_input = data.get('mood_text', '')
        
        if not user_input:
            return jsonify({'error': 'No mood text provided'}), 400
        
        # Check if OpenRouter API key is available
        if not OPENROUTER_API_KEY:
            return jsonify({'error': 'OpenRouter API key not configured. Please set OPENROUTER_API_KEY environment variable.'}), 500
        
        # Analyze mood using OpenRouter
        mood_analysis = analyze_mood_with_llm(user_input)
        
        # Generate playlist recommendations
        playlist_data = generate_playlist_recommendations(mood_analysis)
        
        return jsonify({
            'mood_analysis': mood_analysis,
            'playlist_recommendations': playlist_data
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def analyze_mood_with_llm(user_input):
    """Use OpenRouter to analyze the user's mood and generate recommendations"""
    
    prompt = f"""
    Analyze the following user input and provide mood classification and description:
    
    User Input: "{user_input}"
    
    Please respond in the following JSON format:
    {{
        "primary_mood": "main emotion (e.g., happy, sad, stressed, excited, calm, energetic, melancholic, hopeful)",
        "secondary_mood": "secondary emotion or nuance",
        "mood_description": "one-line description of the emotional state",
        "energy_level": "low/medium/high",
        "tempo_preference": "slow/medium/fast",
        "genre_suggestions": ["genre1", "genre2", "genre3"],
        "mood_keywords": ["keyword1", "keyword2", "keyword3", "keyword4"]
    }}
    
    Focus on creating search-friendly terms that would work well for finding music playlists.
    """
    
    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:5000",
            "X-Title": "Mood-to-Music Recommender"
        }
        
        payload = {
            "model": "openai/gpt-3.5-turbo",  # You can also use "anthropic/claude-3-haiku" or other models
            "messages": [
                {"role": "system", "content": "You are a music mood analyzer. Provide accurate, search-friendly mood classifications."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 300,
            "temperature": 0.7
        }
        
        response = requests.post(
            f"{OPENROUTER_BASE_URL}/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            analysis_text = data['choices'][0]['message']['content']
            
            if analysis_text:
                analysis_text = analysis_text.strip()
            else:
                analysis_text = ""
            
            # Try to extract JSON from the response
            try:
                # Remove any markdown formatting if present
                if analysis_text.startswith('```json'):
                    analysis_text = analysis_text[7:-3]
                elif analysis_text.startswith('```'):
                    analysis_text = analysis_text[3:-3]
                
                mood_data = json.loads(analysis_text)
                return mood_data
                
            except json.JSONDecodeError:
                # Fallback: create a basic structure
                return {
                    "primary_mood": "neutral",
                    "secondary_mood": "calm",
                    "mood_description": "Feeling balanced and content",
                    "energy_level": "medium",
                    "tempo_preference": "medium",
                    "genre_suggestions": ["pop", "indie", "ambient"],
                    "mood_keywords": ["balanced", "content", "peaceful"]
                }
        else:
            print(f"OpenRouter API error: {response.status_code} - {response.text}")
            raise Exception(f"API request failed with status {response.status_code}")
            
    except Exception as e:
        print(f"OpenRouter API error: {e}")
        return {
            "primary_mood": "neutral",
            "secondary_mood": "calm",
            "mood_description": "API error - using fallback mood analysis",
            "energy_level": "medium",
            "tempo_preference": "medium",
            "genre_suggestions": ["pop", "indie", "ambient"],
            "mood_keywords": ["balanced", "content", "peaceful"]
        }

def generate_playlist_recommendations(mood_data):
    """Generate playlist recommendations based on mood analysis"""
    
    primary_mood = mood_data.get('primary_mood', 'neutral')
    energy_level = mood_data.get('energy_level', 'medium')
    genre_suggestions = mood_data.get('genre_suggestions', [])
    mood_keywords = mood_data.get('mood_keywords', [])
    
    # Generate search-friendly playlist titles
    playlist_titles = generate_playlist_titles(primary_mood, energy_level, genre_suggestions, mood_keywords)
    
    # Create YouTube and Spotify search links
    search_queries = create_search_queries(primary_mood, genre_suggestions, mood_keywords)
    
    return {
        'playlist_titles': playlist_titles,
        'search_queries': search_queries,
        'recommended_platforms': ['YouTube Music', 'Spotify', 'Apple Music']
    }

def generate_playlist_titles(primary_mood, energy_level, genre_suggestions, mood_keywords):
    """Generate creative playlist titles based on mood"""
    
    titles = []
    
    # Mood-based titles
    mood_titles = [
        f"{primary_mood.title()} Vibes",
        f"Feeling {primary_mood.title()}",
        f"{primary_mood.title()} Mood",
        f"{primary_mood.title()} Energy"
    ]
    
    # Energy-based titles
    energy_titles = [
        f"{energy_level.title()} Energy {primary_mood.title()}",
        f"{primary_mood.title()} {energy_level.title()} Vibes"
    ]
    
    # Genre-based titles
    for genre in genre_suggestions[:2]:  # Limit to 2 genres
        titles.append(f"{primary_mood.title()} {genre.title()}")
        titles.append(f"{genre.title()} for {primary_mood.title()} Mood")
    
    # Keyword-based titles
    for keyword in mood_keywords[:2]:  # Limit to 2 keywords
        titles.append(f"{keyword.title()} {primary_mood.title()}")
    
    # Combine all titles
    all_titles = mood_titles + energy_titles + titles
    
    # Return unique titles (up to 8)
    return list(dict.fromkeys(all_titles))[:8]

def create_search_queries(primary_mood, genre_suggestions, mood_keywords):
    """Create search queries for different platforms"""
    
    queries = []
    
    # Basic mood searches
    queries.append(f"{primary_mood} music playlist")
    queries.append(f"{primary_mood} songs")
    
    # Genre + mood combinations
    for genre in genre_suggestions[:2]:
        queries.append(f"{genre} {primary_mood} playlist")
        queries.append(f"{primary_mood} {genre} music")
    
    # Keyword combinations
    for keyword in mood_keywords[:2]:
        queries.append(f"{keyword} {primary_mood} music")
    
    return queries[:6]  # Limit to 6 queries

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='127.0.0.1', port=port) 