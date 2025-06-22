from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from openai import OpenAI
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure OpenAI - handle missing API key gracefully
api_key = os.getenv('OPENAI_API_KEY')
if api_key:
    client = OpenAI(api_key=api_key)
else:
    client = None

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
        
        # Check if OpenAI API key is available
        if not client:
            return jsonify({'error': 'OpenAI API key not configured. Please set OPENAI_API_KEY environment variable.'}), 500
        
        # Analyze mood using OpenAI
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
    """Use OpenAI to analyze the user's mood and generate recommendations"""
    
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
        if not client:
            raise Exception("OpenAI client not initialized")
            
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a music mood analyzer. Provide accurate, search-friendly mood classifications."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )
        
        # Parse the JSON response
        analysis_text = response.choices[0].message.content
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
            
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return {
            "primary_mood": "neutral",
            "secondary_mood": "calm",
            "mood_description": "Feeling balanced and content",
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
    app.run(debug=False, host='0.0.0.0', port=port) 