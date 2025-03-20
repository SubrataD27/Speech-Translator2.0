# app.py - Flask Application
from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
from googletrans import Translator
import os
from gtts import gTTS
import uuid
import time

app = Flask(__name__)
translator = Translator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    
    audio_file = request.files['audio']
    target_language = request.form.get('language', 'es')  # Default to Spanish if not specified
    
    # Save the audio file temporarily
    temp_filename = f"temp_{uuid.uuid4()}.wav"
    audio_file.save(temp_filename)
    
    # Initialize recognizer
    recognizer = sr.Recognizer()
    
    try:
        # Convert speech to text
        with sr.AudioFile(temp_filename) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
        
        # Translate the text
        translation = translator.translate(text, dest=target_language)
        
        # Convert translated text to speech
        tts = gTTS(text=translation.text, lang=target_language)
        
        # Generate a unique filename for the translated audio
        translated_filename = f"static/translated_{uuid.uuid4()}.mp3"
        tts.save(translated_filename)
        
        return jsonify({
            'success': True,
            'original_text': text,
            'translated_text': translation.text,
            'audio_url': '/' + translated_filename
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

if __name__ == '__main__':
    os.makedirs('static', exist_ok=True)
    app.run(debug=True)