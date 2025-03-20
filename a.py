# # streamlit_app.py - Streamlit Application
# import streamlit as st
# import speech_recognition as sr
# from googletrans import Translator
# import os
# from gtts import gTTS
# import uuid
# import time
# import base64
# import tempfile

# # Set page configuration
# st.set_page_config(
#     page_title="Real-time Speech Translator",
#     page_icon="🎙️",
#     layout="centered"
# )

# # Custom CSS
# st.markdown("""
# <style>
#     .main {
#         background-color: #f5f9fc;
#     }
#     .stApp {
#         max-width: 800px;
#         margin: 0 auto;
#     }
#     h1 {
#         color: #4a6fa5;
#         text-align: center;
#     }
#     .stButton > button {
#         background-color: #4a6fa5;
#         color: white;
#         border-radius: 50px;
#         padding: 12px 24px;
#         font-size: 16px;
#         font-weight: bold;
#         transition: all 0.3s;
#     }
#     .stButton > button:hover {
#         background-color: #166088;
#         transform: scale(1.05);
#     }
#     .result-box {
#         background-color: #f5f5f5;
#         border-radius: 8px;
#         padding: 15px;
#         border-left: 4px solid #4fc3f7;
#         margin-bottom: 20px;
#     }
#     .result-header {
#         font-weight: bold;
#         color: #4a6fa5;
#         margin-bottom: 10px;
#     }
#     .recording-indicator {
#         animation: pulse 1.5s infinite;
#         color: #f44336;
#         font-weight: bold;
#     }
#     @keyframes pulse {
#         0% { opacity: 1; }
#         50% { opacity: 0.5; }
#         100% { opacity: 1; }
#     }
# </style>
# """, unsafe_allow_html=True)

# # Initialize session state
# if 'translation_results' not in st.session_state:
#     st.session_state.translation_results = []

# # Title and description
# st.title("🎙️ Real-time Speech Translator")
# st.markdown("Speak in English and get instant translations in multiple languages!")

# # Language selection
# languages = {
#     "Spanish": "es",
#     "French": "fr",
#     "German": "de",
#     "Italian": "it",
#     "Portuguese": "pt",
#     "Russian": "ru",
#     "Japanese": "ja",
#     "Korean": "ko",
#     "Chinese (Simplified)": "zh-cn",
#     "Arabic": "ar",
#     "Hindi": "hi"
# }

# selected_language = st.selectbox("Select target language:", list(languages.keys()))
# target_language_code = languages[selected_language]

# # Function to autoplay audio
# def get_audio_player_html(audio_data):
#     audio_base64 = base64.b64encode(audio_data).decode()
#     return f"""
#     <audio autoplay="true" controls>
#         <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
#     </audio>
#     """

# # Function to perform translation
# def translate_audio(audio_data, target_language):
#     # Initialize recognizer
#     recognizer = sr.Recognizer()
    
#     # Save the audio data to a temporary file
#     with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio:
#         temp_audio.write(audio_data)
#         temp_audio_path = temp_audio.name
    
#     try:
#         # Convert speech to text
#         with sr.AudioFile(temp_audio_path) as source:
#             audio = recognizer.record(source)
#             text = recognizer.recognize_google(audio)
        
#         # Translate the text
#         translator = Translator()
#         translation = translator.translate(text, dest=target_language)
        
#         # Convert translated text to speech
#         tts = gTTS(text=translation.text, lang=target_language)
        
#         # Save the translated audio to a temporary file
#         with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_translated_audio:
#             tts.save(temp_translated_audio.name)
            
#             # Read the translated audio file
#             with open(temp_translated_audio.name, 'rb') as f:
#                 translated_audio_data = f.read()
        
#         # Clean up temporary files
#         os.unlink(temp_audio_path)
#         os.unlink(temp_translated_audio.name)
        
#         return {
#             'success': True,
#             'original_text': text,
#             'translated_text': translation.text,
#             'audio_data': translated_audio_data
#         }
    
#     except Exception as e:
#         # Clean up temporary file
#         if os.path.exists(temp_audio_path):
#             os.unlink(temp_audio_path)
        
#         return {
#             'success': False,
#             'error': str(e)
#         }

# # Recording functionality
# col1, col2, col3 = st.columns([1, 2, 1])
# with col2:
#     record_button = st.button("🎙️ Click to Record")

# if record_button:
#     with st.spinner("Recording for 5 seconds..."):
#         # Display recording indicator
#         recording_placeholder = st.empty()
#         recording_placeholder.markdown('<p class="recording-indicator">Recording in progress...</p>', unsafe_allow_html=True)
        
#         # Record audio
#         recognizer = sr.Recognizer()
#         with sr.Microphone() as source:
#             recognizer.adjust_for_ambient_noise(source)
#             audio = recognizer.listen(source, timeout=5)
        
#         recording_placeholder.empty()
        
#         # Process the audio
#         with st.spinner("Translating..."):
#             audio_data = audio.get_wav_data()
#             result = translate_audio(audio_data, target_language_code)
            
#             if result['success']:
#                 # Add result to session state
#                 st.session_state.translation_results.append(result)
#             else:
#                 st.error(f"Error: {result.get('error', 'Unknown error')}")

# # Display translation results
# if st.session_state.translation_results:
#     st.markdown("## Translation Results")
    
#     for i, result in enumerate(reversed(st.session_state.translation_results)):
#         st.markdown(f"""
#         <div class="result-box">
#             <div class="result-header">Original Text (English):</div>
#             <div>{result['original_text']}</div>
#         </div>
#         <div class="result-box">
#             <div class="result-header">Translated Text ({selected_language}):</div>
#             <div>{result['translated_text']}</div>
#         </div>
#         """, unsafe_allow_html=True)
        
#         # Audio player
#         st.markdown("**Listen to translation:**")
#         st.markdown(get_audio_player_html(result['audio_data']), unsafe_allow_html=True)
        
#         if i < len(st.session_state.translation_results) - 1:
#             st.markdown("---")

# # Instructions
# with st.expander("How to use"):
#     st.markdown("""
#     1. Select your target language from the dropdown menu
#     2. Click the "Click to Record" button
#     3. Speak clearly in English for up to 5 seconds
#     4. Wait for the translation to process
#     5. View the text translation and listen to the audio
    
#     **Note:** You need to allow microphone access for this app to work.
#     """)

# # Requirements info
# with st.expander("Installation Requirements"):
#     st.code("""
#     pip install streamlit speech_recognition googletrans==4.0.0-rc1 gtts
    
#     # Run the app with:
#     streamlit run streamlit_app.py
#     """)



















# speech_translator_app.py - Complete Streamlit Speech Translator
# import streamlit as st
# import speech_recognition as sr
# from googletrans import Translator
# import tempfile
# import os
# from gtts import gTTS
# import base64

# # Set page configuration
# st.set_page_config(
#     page_title="Real-time Speech Translator",
#     page_icon="🎙️",
#     layout="centered"
# )

# # Custom CSS
# st.markdown("""
# <style>
#     .main {
#         background-color: #f5f9fc;
#     }
#     .stApp {
#         max-width: 800px;
#         margin: 0 auto;
#     }
#     h1 {
#         color: #4a6fa5;
#         text-align: center;
#     }
#     .stButton > button {
#         background-color: #4a6fa5;
#         color: white;
#         border-radius: 50px;
#         padding: 12px 24px;
#         font-size: 16px;
#         font-weight: bold;
#         transition: all 0.3s;
#     }
#     .stButton > button:hover {
#         background-color: #166088;
#         transform: scale(1.05);
#     }
#     .result-box {
#         background-color: #f5f5f5;
#         border-radius: 8px;
#         padding: 15px;
#         border-left: 4px solid #4fc3f7;
#         margin-bottom: 20px;
#     }
#     .result-header {
#         font-weight: bold;
#         color: #4a6fa5;
#         margin-bottom: 10px;
#     }
#     .recording-indicator {
#         animation: pulse 1.5s infinite;
#         color: #f44336;
#         font-weight: bold;
#     }
#     @keyframes pulse {
#         0% { opacity: 1; }
#         50% { opacity: 0.5; }
#         100% { opacity: 1; }
#     }
# </style>
# """, unsafe_allow_html=True)

# # Function to create an audio player
# def get_audio_player_html(audio_base64):
#     return f"""
#     <audio autoplay="true" controls>
#         <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
#     </audio>
#     """

# # Title and description
# st.title("🎙️ Real-time Speech Translator")
# st.markdown("Speak in English and get instant translations in multiple languages!")

# # Language selection
# languages = {
#     "Spanish": "es",
#     "French": "fr",
#     "German": "de",
#     "Italian": "it",
#     "Portuguese": "pt",
#     "Russian": "ru",
#     "Japanese": "ja",
#     "Korean": "ko",
#     "Chinese (Simplified)": "zh-cn",
#     "Arabic": "ar",
#     "Hindi": "hi"
# }

# selected_language = st.selectbox("Select target language:", list(languages.keys()))
# target_language_code = languages[selected_language]

# # Initialize session state
# if 'translation_results' not in st.session_state:
#     st.session_state.translation_results = []

# # Recording functionality
# col1, col2, col3 = st.columns([1, 2, 1])
# with col2:
#     record_button = st.button("🎙️ Click to Record")

# if record_button:
#     try:
#         with st.spinner("Recording for 5 seconds..."):
#             # Display recording indicator
#             recording_placeholder = st.empty()
#             recording_placeholder.markdown('<p class="recording-indicator">Recording in progress...</p>', unsafe_allow_html=True)
            
#             # Initialize recognizer
#             recognizer = sr.Recognizer()
            
#             # Record audio
#             with sr.Microphone() as source:
#                 st.write("Adjusting for ambient noise...")
#                 recognizer.adjust_for_ambient_noise(source)
#                 st.write("Speak now...")
#                 audio = recognizer.listen(source, timeout=5)
            
#             recording_placeholder.empty()
            
#             # Process the audio
#             with st.spinner("Translating..."):
#                 # Convert speech to text
#                 text = recognizer.recognize_google(audio)
                
#                 # Translate the text
#                 translator = Translator()
#                 translation = translator.translate(text, dest=target_language_code)
                
#                 # Create audio from translated text
#                 with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_audio:
#                     tts = gTTS(text=translation.text, lang=target_language_code)
#                     tts.save(temp_audio.name)
                    
#                     # Read the audio file
#                     with open(temp_audio.name, 'rb') as f:
#                         audio_bytes = f.read()
                    
#                     # Encode audio in base64
#                     audio_base64 = base64.b64encode(audio_bytes).decode()
                
#                 # Clean up temporary file
#                 os.unlink(temp_audio.name)
                
#                 # Store results
#                 st.session_state.translation_results.append({
#                     'original_text': text,
#                     'translated_text': translation.text,
#                     'audio_base64': audio_base64
#                 })
#     except sr.UnknownValueError:
#         st.error("Could not understand audio. Please try again.")
#     except sr.RequestError as e:
#         st.error(f"Could not request results; {e}")
#     except Exception as e:
#         st.error(f"Error: {str(e)}")

# # Display translation results
# if st.session_state.translation_results:
#     st.markdown("## Translation Results")
    
#     for i, result in enumerate(reversed(st.session_state.translation_results)):
#         st.markdown(f"""
#         <div class="result-box">
#             <div class="result-header">Original Text (English):</div>
#             <div>{result['original_text']}</div>
#         </div>
#         <div class="result-box">
#             <div class="result-header">Translated Text ({selected_language}):</div>
#             <div>{result['translated_text']}</div>
#         </div>
#         """, unsafe_allow_html=True)
        
#         # Audio player
#         st.markdown("**Listen to translation:**")
#         st.markdown(get_audio_player_html(result['audio_base64']), unsafe_allow_html=True)
        
#         if i < len(st.session_state.translation_results) - 1:
#             st.markdown("---")

# # Instructions
# with st.expander("How to use"):
#     st.markdown("""
#     1. Select your target language from the dropdown menu
#     2. Click the "Click to Record" button
#     3. Speak clearly in English for up to 5 seconds
#     4. Wait for the translation to process
#     5. View the text translation and listen to the audio
    
#     **Note:** Make sure your microphone is working and browser permissions are granted.
#     """)

# # Installation instructions
# with st.expander("Installation Instructions"):
#     st.markdown("""
#     ### One-time setup:
    
#     1. Install required packages:
#     ```
#     pip install streamlit==1.15.0 SpeechRecognition==3.8.1 googletrans==4.0.0-rc1 gTTS==2.2.3 pyaudio
#     ```
    
#     2. Run the application:
#     ```
#     streamlit run speech_translator_app.py
#     ```
    
#     3. A browser window will automatically open with the application running.
#     """)

# # Add footer
# st.markdown("---")
# st.markdown("Created with ❤️ using Streamlit, Google Translate, and gTTS")































import streamlit as st
import speech_recognition as sr
from googletrans import Translator
import tempfile
import os
from gtts import gTTS
import base64

# Set page configuration
st.set_page_config(page_title="🎙️ Real-time Speech Translator", page_icon="🌍", layout="centered")

# Custom Styling
st.markdown("""
    <style>
        body {
            background-color: #f7f9fc;
        }
        .stApp {
            max-width: 700px;
            margin: auto;
        }
        .title {
            font-size: 26px;
            font-weight: bold;
            color: #2c3e50;
            text-align: center;
        }
        .btn-custom {
            background-color: #2c3e50 !important;
            color: white !important;
            border-radius: 10px;
            font-weight: bold;
            padding: 10px 20px;
            transition: all 0.3s;
        }
        .btn-custom:hover {
            background-color: #34495e !important;
        }
    </style>
""", unsafe_allow_html=True)

# Page Title
st.markdown('<p class="title">🎙️ Real-time Speech Translator</p>', unsafe_allow_html=True)

# Language Selection
languages = {
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
    "Russian": "ru",
    "Japanese": "ja",
    "Korean": "ko",
    "Chinese (Simplified)": "zh-cn",
    "Arabic": "ar",
    "Hindi": "hi"
}

selected_language = st.selectbox("🌍 Select target language:", list(languages.keys()))
target_language_code = languages[selected_language]

# Initialize Session State
if 'translation_results' not in st.session_state:
    st.session_state.translation_results = []

# Function to generate audio player

def get_audio_player(audio_base64):
    return f"""
    <audio autoplay controls>
        <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
    </audio>
    """

# Recording Section
if st.button("🎤 Start Recording", key='record', help="Click to start recording your speech"):
    try:
        with st.spinner("🎙️ Recording for 5 seconds..."):
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=5)

        with st.spinner("🔍 Processing & Translating..."):
            text = recognizer.recognize_google(audio)
            translator = Translator()
            translation = translator.translate(text, dest=target_language_code)

            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_audio:
                tts = gTTS(text=translation.text, lang=target_language_code)
                tts.save(temp_audio.name)
                
                with open(temp_audio.name, 'rb') as f:
                    audio_bytes = f.read()
                
                audio_base64 = base64.b64encode(audio_bytes).decode()

            os.unlink(temp_audio.name)
            
            st.session_state.translation_results.append({
                'original_text': text,
                'translated_text': translation.text,
                'audio_base64': audio_base64
            })
    except sr.UnknownValueError:
        st.error("❌ Could not understand the speech. Try again.")
    except sr.RequestError as e:
        st.error(f"❌ Speech recognition request failed: {e}")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

# Display Translations
if st.session_state.translation_results:
    st.subheader("📝 Translation Results")
    for result in reversed(st.session_state.translation_results):
        st.markdown(f"**Original (English):** {result['original_text']}")
        st.markdown(f"**Translated ({selected_language}):** {result['translated_text']}")
        st.markdown(get_audio_player(result['audio_base64']), unsafe_allow_html=True)
        st.markdown("---")

# Instructions
with st.expander("ℹ️ How to Use"):
    st.markdown("""
    1. Select your target language.
    2. Click the 'Start Recording' button.
    3. Speak clearly in English.
    4. The system will process and translate your speech.
    5. Read and listen to the translation.
    """)

# Installation Instructions
with st.expander("⚙️ Installation Guide"):
    st.markdown("""
    **Run the following commands:**
    ```bash
    pip install streamlit SpeechRecognition googletrans==4.0.0-rc1 gTTS pyaudio
    ```
    Then run:
    ```bash
    streamlit run speech_translator_app.py
    ```
    """)

st.markdown("---")
st.markdown("✅ **Built with ❤️ using Streamlit, SpeechRecognition, Google Translate, and gTTS**")
