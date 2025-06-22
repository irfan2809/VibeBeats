from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Mood-to-music mapping
MOOD_MUSIC_MAP = {
    'happy': {
        'primary_mood': 'happy',
        'secondary_mood': 'joyful',
        'mood_description': 'Feeling cheerful and upbeat',
        'energy_level': 'high',
        'tempo_preference': 'fast',
        'genre_suggestions': ['pop', 'dance', 'reggae', 'disco'],
        'mood_keywords': ['upbeat', 'energetic', 'cheerful', 'positive']
    },
    'sad': {
        'primary_mood': 'sad',
        'secondary_mood': 'melancholic',
        'mood_description': 'Feeling down and reflective',
        'energy_level': 'low',
        'tempo_preference': 'slow',
        'genre_suggestions': ['blues', 'jazz', 'indie', 'folk'],
        'mood_keywords': ['melancholic', 'reflective', 'calm', 'peaceful']
    },
    'excited': {
        'primary_mood': 'excited',
        'secondary_mood': 'energetic',
        'mood_description': 'Feeling pumped and energetic',
        'energy_level': 'high',
        'tempo_preference': 'fast',
        'genre_suggestions': ['rock', 'electronic', 'hip-hop', 'metal'],
        'mood_keywords': ['energetic', 'powerful', 'intense', 'dynamic']
    },
    'calm': {
        'primary_mood': 'calm',
        'secondary_mood': 'peaceful',
        'mood_description': 'Feeling relaxed and at ease',
        'energy_level': 'low',
        'tempo_preference': 'slow',
        'genre_suggestions': ['ambient', 'classical', 'lofi', 'nature'],
        'mood_keywords': ['relaxing', 'peaceful', 'soothing', 'tranquil']
    },
    'stressed': {
        'primary_mood': 'stressed',
        'secondary_mood': 'anxious',
        'mood_description': 'Feeling tense and overwhelmed',
        'energy_level': 'medium',
        'tempo_preference': 'medium',
        'genre_suggestions': ['chill', 'ambient', 'piano', 'acoustic'],
        'mood_keywords': ['soothing', 'calming', 'gentle', 'therapeutic']
    }
}

def generate_playlist_recommendations(mood_data):
    """Generate playlist recommendations based on mood analysis"""
    
    primary_mood = mood_data.get('primary_mood', 'happy')
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

@app.route('/')
def index():
    return render_template('button_index.html')

@app.route('/analyze_mood', methods=['POST'])
def analyze_mood():
    try:
        data = request.get_json()
        selected_mood = data.get('mood', '')
        
        if not selected_mood:
            return jsonify({'error': 'No mood selected'}), 400
        
        # Get mood data based on selection
        if selected_mood in MOOD_MUSIC_MAP:
            mood_analysis = MOOD_MUSIC_MAP[selected_mood]
        else:
            return jsonify({'error': 'Invalid mood selection'}), 400
        
        # Generate playlist recommendations
        playlist_data = generate_playlist_recommendations(mood_analysis)
        
        return jsonify({
            'mood_analysis': mood_analysis,
            'playlist_recommendations': playlist_data
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='127.0.0.1', port=port) 