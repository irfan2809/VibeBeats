from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import os
import base64
import json

app = Flask(__name__)
CORS(app)

# Spotify API credentials (free tier)
SPOTIFY_CLIENT_ID = "your_spotify_client_id"  # Get from https://developer.spotify.com/
SPOTIFY_CLIENT_SECRET = "your_spotify_client_secret"

# Mood to Spotify playlist mapping
MOOD_PLAYLISTS = {
    'happy': [
        'spotify:playlist:37i9dQZF1DX3rxVfibe1L0',  # Happy Hits
        'spotify:playlist:37i9dQZF1DX9XIFQuFvzMp',  # Feel Good Pop
        'spotify:playlist:37i9dQZF1DXdPec7aLTmlC'   # Dance Pop
    ],
    'sad': [
        'spotify:playlist:37i9dQZF1DX7qK8ma5wgG1',  # Sad Songs
        'spotify:playlist:37i9dQZF1DX3YSRoSdA634',  # Melancholy
        'spotify:playlist:37i9dQZF1DX5Vy6DFOcx00'   # Rainy Day
    ],
    'excited': [
        'spotify:playlist:37i9dQZF1DX76Wlfdnj7AP',  # Beast Mode
        'spotify:playlist:37i9dQZF1DX0XUsuxWHRQd',  # RapCaviar
        'spotify:playlist:37i9dQZF1DX5Vy6DFOcx00'   # Rock Classics
    ],
    'calm': [
        'spotify:playlist:37i9dQZF1DX3Ogo9pFvBkY',  # Ambient Relaxation
        'spotify:playlist:37i9dQZF1DX4sWSpwq3LiO',  # Peaceful Piano
        'spotify:playlist:37i9dQZF1DX4sWSpwq3LiO'   # Sleep
    ],
    'stressed': [
        'spotify:playlist:37i9dQZF1DX4sWSpwq3LiO',  # Stress Relief
        'spotify:playlist:37i9dQZF1DX3Ogo9pFvBkY',  # Calm Down
        'spotify:playlist:37i9dQZF1DX4sWSpwq3LiO'   # Mindfulness
    ]
}

def get_spotify_token():
    """Get Spotify access token"""
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_header = base64.b64encode(f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}".encode()).decode()
    
    headers = {
        'Authorization': f'Basic {auth_header}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    data = {'grant_type': 'client_credentials'}
    
    response = requests.post(auth_url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json()['access_token']
    return None

def get_spotify_recommendations(mood):
    """Get Spotify recommendations based on mood"""
    token = get_spotify_token()
    if not token:
        return get_fallback_recommendations(mood)
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # Get playlists for the mood
    playlists = MOOD_PLAYLISTS.get(mood, MOOD_PLAYLISTS['happy'])
    
    recommendations = {
        'playlists': [],
        'tracks': [],
        'artists': []
    }
    
    # Get playlist details
    for playlist_id in playlists[:2]:
        try:
            playlist_url = f"https://api.spotify.com/v1/playlists/{playlist_id.split(':')[-1]}"
            response = requests.get(playlist_url, headers=headers)
            if response.status_code == 200:
                playlist_data = response.json()
                recommendations['playlists'].append({
                    'name': playlist_data['name'],
                    'url': playlist_data['external_urls']['spotify'],
                    'tracks': len(playlist_data['tracks']['items'])
                })
        except:
            continue
    
    return recommendations

def get_fallback_recommendations(mood):
    """Fallback recommendations without API"""
    fallback_data = {
        'happy': {
            'description': 'Upbeat and cheerful music',
            'playlists': ['Happy Hits', 'Feel Good Vibes', 'Summer Party'],
            'artists': ['Pharrell Williams', 'Bruno Mars', 'Daft Punk'],
            'search_queries': ['happy music playlist', 'upbeat songs', 'feel good music']
        },
        'sad': {
            'description': 'Melancholic and reflective music',
            'playlists': ['Sad Songs', 'Melancholy Vibes', 'Rainy Day'],
            'artists': ['Adele', 'Ed Sheeran', 'Lana Del Rey'],
            'search_queries': ['sad songs playlist', 'melancholy music', 'heartbreak songs']
        },
        'excited': {
            'description': 'High energy and powerful music',
            'playlists': ['Workout Mix', 'Party Anthems', 'Rock Classics'],
            'artists': ['Imagine Dragons', 'The Weeknd', 'Eminem'],
            'search_queries': ['workout music', 'party songs', 'energy boost']
        },
        'calm': {
            'description': 'Relaxing and peaceful music',
            'playlists': ['Study Music', 'Sleep Sounds', 'Meditation'],
            'artists': ['Ludovico Einaudi', 'Max Richter', 'Chillhop Music'],
            'search_queries': ['study music', 'sleep sounds', 'meditation music']
        },
        'stressed': {
            'description': 'Soothing and therapeutic music',
            'playlists': ['Stress Relief', 'Calm Down', 'Therapeutic Sounds'],
            'artists': ['Ólafur Arnalds', 'Nils Frahm', 'Sigur Rós'],
            'search_queries': ['stress relief music', 'calm down songs', 'therapeutic sounds']
        }
    }
    
    return fallback_data.get(mood, fallback_data['happy'])

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
        
        # Get recommendations
        recommendations = get_fallback_recommendations(selected_mood)
        
        # Format response
        mood_analysis = {
            'primary_mood': selected_mood,
            'secondary_mood': 'music-focused',
            'mood_description': recommendations['description'],
            'energy_level': 'medium',
            'tempo_preference': 'medium',
            'genre_suggestions': ['Pop', 'Rock', 'Electronic'],
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