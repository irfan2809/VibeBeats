from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import os
import random

app = Flask(__name__)
CORS(app)

# Free music APIs and data
MUSIC_DATA = {
    'happy': {
        'description': 'Upbeat and cheerful music',
        'genres': ['Pop', 'Dance', 'Reggae', 'Disco'],
        'artists': ['Pharrell Williams', 'Bruno Mars', 'Daft Punk', 'The Beatles'],
        'songs': ['Happy', 'Uptown Funk', 'Get Lucky', 'Here Comes the Sun'],
        'playlists': ['Happy Hits', 'Feel Good Vibes', 'Summer Party', 'Dance Pop']
    },
    'sad': {
        'description': 'Melancholic and reflective music',
        'genres': ['Blues', 'Jazz', 'Indie', 'Folk'],
        'artists': ['Adele', 'Ed Sheeran', 'Lana Del Rey', 'Bon Iver'],
        'songs': ['Someone Like You', 'Thinking Out Loud', 'Summertime Sadness', 'Skinny Love'],
        'playlists': ['Sad Songs', 'Melancholy Vibes', 'Rainy Day', 'Heartbreak']
    },
    'excited': {
        'description': 'High energy and powerful music',
        'genres': ['Rock', 'Electronic', 'Hip-Hop', 'Metal'],
        'artists': ['Imagine Dragons', 'The Weeknd', 'Eminem', 'Metallica'],
        'songs': ['Radioactive', 'Blinding Lights', 'Lose Yourself', 'Nothing Else Matters'],
        'playlists': ['Workout Mix', 'Party Anthems', 'Rock Classics', 'Energy Boost']
    },
    'calm': {
        'description': 'Relaxing and peaceful music',
        'genres': ['Ambient', 'Classical', 'Lo-Fi', 'Nature'],
        'artists': ['Ludovico Einaudi', 'Max Richter', 'Chillhop Music', 'Nature Sounds'],
        'songs': ['Experience', 'On the Nature of Daylight', 'Chill Beats', 'Ocean Waves'],
        'playlists': ['Study Music', 'Sleep Sounds', 'Meditation', 'Peaceful Vibes']
    },
    'stressed': {
        'description': 'Soothing and therapeutic music',
        'genres': ['Chill', 'Ambient', 'Piano', 'Acoustic'],
        'artists': ['Ólafur Arnalds', 'Nils Frahm', 'Sigur Rós', 'Explosions in the Sky'],
        'songs': ['Near Light', 'Says', 'Hoppípolla', 'Your Hand in Mine'],
        'playlists': ['Stress Relief', 'Calm Down', 'Therapeutic Sounds', 'Mindfulness']
    }
}

def get_music_recommendations(mood):
    """Get music recommendations based on mood"""
    if mood not in MUSIC_DATA:
        mood = 'happy'  # Default fallback
    
    data = MUSIC_DATA[mood]
    
    # Generate search queries for different platforms
    search_queries = []
    
    # Genre searches
    for genre in data['genres'][:2]:
        search_queries.append(f"{genre} {mood} playlist")
        search_queries.append(f"{mood} {genre} music")
    
    # Artist searches
    for artist in data['artists'][:2]:
        search_queries.append(f"{artist} {mood} songs")
    
    # Song searches
    for song in data['songs'][:2]:
        search_queries.append(f"{song} {mood} mood")
    
    # Playlist searches
    for playlist in data['playlists'][:2]:
        search_queries.append(f"{playlist} {mood}")
    
    return {
        'mood_description': data['description'],
        'genres': data['genres'],
        'artists': data['artists'],
        'songs': data['songs'],
        'playlists': data['playlists'],
        'search_queries': search_queries[:6]
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze_mood', methods=['POST'])
def analyze_mood():
    try:
        data = request.get_json()
        selected_mood = data.get('mood', '')
        
        if not selected_mood:
            return jsonify({'error': 'No mood selected'}), 400
        
        # Get music recommendations
        recommendations = get_music_recommendations(selected_mood)
        
        # Format response to match expected structure
        mood_analysis = {
            'primary_mood': selected_mood,
            'secondary_mood': 'music-focused',
            'mood_description': recommendations['mood_description'],
            'energy_level': 'medium',
            'tempo_preference': 'medium',
            'genre_suggestions': recommendations['genres'],
            'mood_keywords': [selected_mood, 'music', 'playlist']
        }
        
        playlist_recommendations = {
            'playlist_titles': recommendations['playlists'],
            'search_queries': recommendations['search_queries'],
            'recommended_platforms': ['YouTube Music', 'Spotify', 'Apple Music']
        }
        
        return jsonify({
            'mood_analysis': mood_analysis,
            'playlist_recommendations': playlist_recommendations
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='127.0.0.1', port=port) 