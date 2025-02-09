from flask import Flask, render_template, request, jsonify
import requests
from flask_cors import CORS  # Import CORS
import google.generativeai as genai

# Initialize the client with your API key
genai.configure(api_key="AIzaSyDzU6uAm9R2d2UIL3Wb7rl3TCsH9p78xOE")

model = genai.GenerativeModel('gemini-pro')

# Generate content using the Gemini model
# response = genai.generate_content(
#     model="gemini-2.0-flash",
#     contents="Explain how AI works",
# )
response = model.generate_content("Explain how AI works")

print(response.text)
app = Flask(__name__)
CORS(app)
# Define the Gemini API endpoint and your API key (replace with your actual key)
# client = genai.Client(api_key="")

# Map emojis to moods
emoji_to_mood = {
    "😀": "happy",
    "😢": "sad",
    "😎": "cool",
    "😠": "angry",
    "😌": "relaxed",
    "🥳": "excited",
    # Add more emojis and moods as needed
}

# Function to get song suggestions from Gemini API based on mood
def get_song_suggestions(mood):
    try:
        # response = genai.generate_content(
        # model="gemini-2.0-flash",
        # contents="Suggest songd for this mood : "+mood
        # )
        response = model.generate_content("Suggest songs for this mood"+mood)
        print(response.text)
        # response = requests.get(GEMINI_API_URL, params={"mood": mood, "api_key": GEMINI_API_KEY})
        # response.raise_for_status()  # Check for request errors
        songs = response.text
        return songs
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Gemini API: {e}")
        return []

@app.route('/')
def index():
    return render_template('index2.html')

@app.route('/get_songs', methods=['POST', 'OPTIONS'])
def get_songs():
    emoji = request.json.get('emoji')
    mood = emoji_to_mood.get(emoji, "neutral")  # Default to neutral if emoji not found
    
    # Fetch song suggestions based on the mapped mood
    songs = get_song_suggestions(mood)
    
    # Return the song suggestions as JSON
    return songs


if __name__ == '__main__':
    app.run(debug=True,port=8000)
