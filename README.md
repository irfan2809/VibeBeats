# 🎵 Mood-to-Music Recommender

A smart web application that analyzes your mood through text input and recommends personalized music playlists and search terms for various music platforms.

## ✨ Features

- **Mood Analysis**: Uses OpenAI's GPT to intelligently analyze your emotional state
- **Smart Recommendations**: Generates search-friendly playlist titles and search terms
- **Multi-Platform Support**: Provides direct links to Spotify, YouTube Music, and Apple Music
- **Beautiful UI**: Modern, responsive design with smooth animations
- **Real-time Analysis**: Instant mood classification and music recommendations

## 🚀 How It Works

1. **Input Your Mood**: Describe how you're feeling in natural language
   - "I'm feeling a little stressed but hopeful about the future"
   - "I'm in a great mood and want to dance"
   - "Feeling melancholic and reflective"

2. **AI Analysis**: The LLM analyzes your text and extracts:
   - Primary and secondary moods
   - Energy level and tempo preferences
   - Genre suggestions
   - Mood keywords

3. **Music Recommendations**: Get personalized:
   - Creative playlist titles
   - Search terms for music platforms
   - Direct links to find music

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.7 or higher
- OpenAI API key

### Installation

1. **Clone or download this project**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your OpenAI API key**:
   - Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)
   - Create a `.env` file in the project root
   - Add your API key:
     ```
     OPENAI_API_KEY=your_actual_api_key_here
     ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Open your browser** and go to `http://localhost:5000`

## 📁 Project Structure

```
Music recommender/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Web interface
├── env_example.txt       # Environment variables example
└── README.md            # This file
```

## 🎯 Example Usage

### Input Examples:
- "I'm feeling anxious and need something calming"
- "Super excited and want to celebrate!"
- "Feeling nostalgic and want to reminisce"
- "Stressed from work, need something uplifting"

### Output Examples:
- **Mood Analysis**: "Feeling anxious with a need for calm"
- **Playlist Titles**: "Calm Vibes", "Anxious Ambient", "Peaceful Energy"
- **Search Terms**: "anxious calming music", "ambient anxiety relief", "peaceful stress relief"

## 🔧 Technical Details

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **AI**: OpenAI GPT-3.5-turbo
- **Styling**: Custom CSS with gradients and animations
- **Responsive**: Works on desktop and mobile devices

## 🎨 Features in Detail

### Mood Analysis
- Extracts primary and secondary emotions
- Determines energy level (low/medium/high)
- Suggests tempo preferences
- Identifies relevant music genres
- Generates search-friendly keywords

### Playlist Generation
- Creates 8 unique playlist titles
- Combines mood, energy, and genre elements
- Optimized for music platform searches

### Platform Integration
- **Spotify**: Direct search links
- **YouTube Music**: Direct search links  
- **Apple Music**: Direct search links
- Click any search term to open in your preferred platform

## 🤝 Contributing

Feel free to contribute to this project! Some ideas:
- Add more music platforms
- Implement music player integration
- Add mood history tracking
- Create user accounts and saved playlists

## 📝 License

This project is open source and available under the MIT License.

## 🆘 Troubleshooting

### Common Issues:

1. **"OpenAI API error"**
   - Check your API key is correct
   - Ensure you have credits in your OpenAI account
   - Verify the `.env` file is in the project root

2. **"Module not found" errors**
   - Run `pip install -r requirements.txt`
   - Check Python version (3.7+ required)

3. **Port already in use**
   - Change the port in `app.py` line: `app.run(debug=True, host='0.0.0.0', port=5001)`

## 🎵 Enjoy Your Music!

This application helps you discover the perfect music for any mood. Whether you're feeling happy, sad, stressed, or excited, let AI guide you to the right tunes! 🎶 