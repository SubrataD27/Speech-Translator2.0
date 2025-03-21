# import streamlit as st
# import speech_recognition as sr
# from deep_translator import GoogleTranslator
# from gtts import gTTS
# import base64
# import os
# import tempfile
# import time
# from io import BytesIO
# import uuid
# import nltk
# from nltk.tokenize import sent_tokenize
# import string
# import json
# import vosk
# import wave
# import numpy as np

# # Download NLTK data (only needed first time)
# try:
#     nltk.data.find('tokenizers/punkt')
# except LookupError:
#     nltk.download('punkt')

# # ---------------------- Page Configuration ----------------------
# st.set_page_config(
#     page_title="Real-Time Speech Translator",
#     page_icon="🎙️",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# # ---------------------- Custom CSS for Dark Mode UI ----------------------
# st.markdown("""
# <style>
# /* Main container styling */
# .main {
#     background-color: #121212;
#     color: #e0e0e0;
# }

# /* Custom container */
# .custom-container {
#     background-color: #1e1e1e;
#     border-radius: 12px;
#     padding: 24px;
#     box-shadow: 0 4px 15px rgba(0,0,0,0.3);
#     margin-bottom: 24px;
#     border: 1px solid #333;
# }

# /* Header styling */
# .main-header {
#     font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
#     font-weight: 800;
#     font-size: 42px;
#     margin-bottom: 0;
#     text-align: center;
#     background: linear-gradient(90deg, #4776E6 0%, #8E54E9 100%);
#     -webkit-background-clip: text;
#     -webkit-text-fill-color: transparent;
#     padding: 10px 0;
# }

# .subtitle {
#     font-size: 18px;
#     color: #a0a0a0;
#     text-align: center;
#     margin-bottom: 20px;
# }

# /* Recording button */
# .stButton > button {
#     width: 100%;
#     background: linear-gradient(90deg, #4776E6 0%, #8E54E9 100%);
#     color: white;
#     font-weight: bold;
#     font-size: 18px;
#     padding: 15px 0;
#     border: none;
#     border-radius: 8px;
#     transition: all 0.3s ease;
# }

# .stButton > button:hover {
#     background: linear-gradient(90deg, #3A67D7 0%, #7F45DA 100%);
#     transform: translateY(-2px);
#     box-shadow: 0 4px 15px rgba(71, 118, 230, 0.5);
# }

# /* Status indicators */
# .status-recording {
#     color: #ff4d4d;
#     font-weight: bold;
#     animation: pulse 1.5s infinite;
# }

# .status-processing {
#     color: #ffa64d;
#     font-weight: bold;
# }

# .status-success {
#     color: #4dff4d;
#     font-weight: bold;
# }

# /* Results containers */
# .result-box {
#     background-color: #252525;
#     border-radius: 8px;
#     padding: 20px;
#     border-left: 5px solid #4776E6;
#     margin-bottom: 15px;
# }

# .result-box-header {
#     font-weight: bold;
#     color: #4776E6;
#     margin-bottom: 10px;
#     font-size: 18px;
# }

# .result-text {
#     line-height: 1.6;
#     font-size: 16px;
#     color: #e0e0e0;
# }

# /* Language selector */
# .language-header {
#     font-weight: 600;
#     color: #a0a0a0;
#     margin-bottom: 8px;
# }

# /* API Selector */
# .api-selector {
#     background-color: #252525;
#     padding: 16px;
#     border-radius: 12px;
#     margin-bottom: 15px;
#     border: 1px solid #333;
# }

# /* Audio player */
# audio {
#     width: 100%;
#     border-radius: 30px;
#     background-color: #333;
# }

# /* Metrics */
# .metric-container {
#     background-color: #252525;
#     border-radius: 12px;
#     padding: 15px;
#     text-align: center;
#     box-shadow: 0 2px 8px rgba(0,0,0,0.2);
#     border: 1px solid #333;
# }

# .metric-value {
#     font-size: 24px;
#     font-weight: bold;
#     color: #4776E6;
# }

# .metric-label {
#     font-size: 14px;
#     color: #a0a0a0;
# }

# /* Animation */
# @keyframes pulse {
#     0% { opacity: 1; }
#     50% { opacity: 0.5; }
#     100% { opacity: 1; }
# }

# /* Footer */
# .footer {
#     text-align: center;
#     color: #a0a0a0;
#     font-size: 14px;
#     margin-top: 30px;
#     padding-top: 10px;
#     border-top: 1px solid #333;
# }

# /* Error notification */
# .error-notification {
#     background-color: #330000;
#     border-left: 5px solid #ff4d4d;
#     padding: 15px;
#     border-radius: 8px;
#     margin-bottom: 20px;
#     color: #ff9999;
# }

# /* Success notification */
# .success-notification {
#     background-color: #003300;
#     border-left: 5px solid #4dff4d;
#     padding: 15px;
#     border-radius: 8px;
#     margin-bottom: 20px;
#     color: #99ff99;
# }

# /* Info notification */
# .info-notification {
#     background-color: #000033;
#     border-left: 5px solid #4d4dff;
#     padding: 15px;
#     border-radius: 8px;
#     margin-bottom: 20px;
#     color: #9999ff;
# }

# /* Tabs */
# .stTabs [data-baseweb="tab-list"] {
#     gap: 8px;
#     background-color: #1e1e1e;
#     border-radius: 8px;
#     padding: 5px;
# }

# .stTabs [data-baseweb="tab"] {
#     height: 50px;
#     border-radius: 6px;
#     padding: 0 20px;
#     background-color: #252525;
#     color: #e0e0e0;
# }

# .stTabs [aria-selected="true"] {
#     background-color: #4776E6 !important;
#     color: white !important;
# }

# /* Text inputs */
# div[data-baseweb="input"] {
#     background-color: #252525 !important;
#     border: 1px solid #333 !important;
#     border-radius: 8px !important;
# }

# div[data-baseweb="input"] input {
#     color: #e0e0e0 !important;
# }

# /* Select boxes */
# div[data-baseweb="select"] {
#     background-color: #252525 !important;
#     border: 1px solid #333 !important;
#     border-radius: 8px !important;
# }

# div[data-baseweb="select"] div[data-testid="stMarkdownContainer"] {
#     color: #e0e0e0 !important;
# }

# /* Checkbox */
# .stCheckbox label {
#     color: #e0e0e0 !important;
# }

# /* Expander */
# .streamlit-expanderHeader {
#     background-color: #252525 !important;
#     color: #e0e0e0 !important;
#     border-radius: 8px !important;
# }

# .streamlit-expanderContent {
#     background-color: #1e1e1e !important;
#     color: #e0e0e0 !important;
#     border-radius: 0 0 8px 8px !important;
# }

# /* Scrollbar */
# ::-webkit-scrollbar {
#     width: 10px;
#     height: 10px;
# }

# ::-webkit-scrollbar-track {
#     background: #1e1e1e;
# }

# ::-webkit-scrollbar-thumb {
#     background: #4776E6;
#     border-radius: 5px;
# }

# ::-webkit-scrollbar-thumb:hover {
#     background: #8E54E9;
# }
# </style>
# """, unsafe_allow_html=True)

# # Helper function to get audio playback HTML
# def get_audio_player_html(audio_bytes):
#     """Generate HTML for audio player with custom styling"""
#     b64 = base64.b64encode(audio_bytes).decode()
#     return f"""
#     <audio controls autoplay="true">
#         <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
#     </audio>
#     """

# # ---------------------- Initialize Session State ----------------------
# if 'history' not in st.session_state:
#     st.session_state.history = []
# if 'processing_time' not in st.session_state:
#     st.session_state.processing_time = 0
# if 'translation_count' not in st.session_state:
#     st.session_state.translation_count = 0
# if 'vosk_model' not in st.session_state:
#     st.session_state.vosk_model = None
# if 'model_loaded' not in st.session_state:
#     st.session_state.model_loaded = False

# # ---------------------- Vosk Model Download ----------------------
# def download_vosk_model():
#     """Download and initialize Vosk model for offline speech recognition"""
#     try:
#         import requests
#         from tqdm import tqdm
#         import zipfile
#         import os
        
#         # Create models directory if it doesn't exist
#         if not os.path.exists("models"):
#             os.makedirs("models")
        
#         # Check if model already exists
#         if os.path.exists("models/vosk-model-small-en-us-0.15"):
#             st.session_state.model_loaded = True
#             return True
        
#         # URL for small English model
#         model_url = "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip"
#         zip_path = "models/vosk-model-small-en-us-0.15.zip"
        
#         # Download the model
#         with st.spinner("Downloading speech recognition model (this may take a few minutes)..."):
#             response = requests.get(model_url, stream=True)
#             total_size = int(response.headers.get('content-length', 0))
            
#             with open(zip_path, 'wb') as file, tqdm(
#                 desc="Downloading model",
#                 total=total_size,
#                 unit='B',
#                 unit_scale=True,
#                 unit_divisor=1024,
#             ) as bar:
#                 for data in response.iter_content(chunk_size=1024):
#                     size = file.write(data)
#                     bar.update(size)
        
#         # Extract the model
#         with st.spinner("Extracting model..."):
#             with zipfile.ZipFile(zip_path, 'r') as zip_ref:
#                 zip_ref.extractall("models/")
            
#             # Remove the zip file to save space
#             os.remove(zip_path)
        
#         st.session_state.model_loaded = True
#         return True
    
#     except Exception as e:
#         st.error(f"Error downloading model: {str(e)}")
#         return False

# def transcribe_audio_with_vosk(audio_data):
#     """Transcribe audio using Vosk (offline speech recognition)"""
#     try:
#         if not st.session_state.model_loaded:
#             success = download_vosk_model()
#             if not success:
#                 return "Error loading speech recognition model."
        
#         # Initialize Vosk model if not already done
#         if st.session_state.vosk_model is None:
#             from vosk import Model, KaldiRecognizer
#             model_path = "models/vosk-model-small-en-us-0.15"
#             st.session_state.vosk_model = Model(model_path)
        
#         # Create a temporary WAV file
#         with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_wav:
#             temp_wav_path = temp_wav.name
#             temp_wav.write(audio_data)
        
#         # Process with Vosk
#         from vosk import Model, KaldiRecognizer
#         wf = wave.open(temp_wav_path, "rb")
        
#         # Check if audio format is compatible
#         if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
#             # Convert to compatible format if needed
#             import subprocess
#             output_path = temp_wav_path + "_converted.wav"
#             subprocess.run(['ffmpeg', '-i', temp_wav_path, '-acodec', 'pcm_s16le', '-ac', '1', '-ar', '16000', output_path], 
#                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
#             wf.close()
#             wf = wave.open(output_path, "rb")
        
#         rec = KaldiRecognizer(st.session_state.vosk_model, wf.getframerate())
#         rec.SetWords(True)
        
#         results = []
#         while True:
#             data = wf.readframes(4000)
#             if len(data) == 0:
#                 break
#             if rec.AcceptWaveform(data):
#                 part_result = json.loads(rec.Result())
#                 results.append(part_result.get('text', ''))
        
#         part_result = json.loads(rec.FinalResult())
#         results.append(part_result.get('text', ''))
        
#         # Clean up temporary files
#         wf.close()
#         os.unlink(temp_wav_path)
#         if os.path.exists(temp_wav_path + "_converted.wav"):
#             os.unlink(temp_wav_path + "_converted.wav")
        
#         return " ".join(results).strip()
    
#     except Exception as e:
#         return f"Error in speech recognition: {str(e)}"

# def enhance_translation(text, target_language):
#     """Enhance translation using basic NLP techniques (free alternative to Cohere)"""
#     # Split into sentences
#     sentences = sent_tokenize(text)
    
#     # Basic enhancements
#     enhanced_sentences = []
#     for sentence in sentences:
#         # Capitalize first letter of each sentence
#         if sentence and len(sentence) > 0:
#             sentence = sentence[0].upper() + sentence[1:]
        
#         # Ensure proper punctuation
#         if sentence and len(sentence) > 0 and sentence[-1] not in string.punctuation:
#             sentence += '.'
#         # Add to enhanced sentences
#         enhanced_sentences.append(sentence)
    
#     # Join sentences with proper spacing
#     enhanced_text = ' '.join(enhanced_sentences)
    
#     # Remove double spaces
#     enhanced_text = ' '.join(enhanced_text.split())
    
#     return enhanced_text

# # ---------------------- UI Components ----------------------
# def render_header():
#     """Render the application header"""
#     st.markdown('<h1 class="main-header">Real-Time Speech Translator 🎙️</h1>', unsafe_allow_html=True)
#     st.markdown('<p class="subtitle">Powered by Vosk & Google Translate - Free & Offline Speech Translation</p>', unsafe_allow_html=True)

# def render_language_selector():
#     """Render language selection interface"""
#     st.markdown('<p class="language-header">🌍 Target Language</p>', unsafe_allow_html=True)
#     languages = {
#         "Spanish": "es",
#         "French": "fr",
#         "German": "de",
#         "Italian": "it",
#         "Portuguese": "pt",
#         "Russian": "ru",
#         "Japanese": "ja",
#         "Korean": "ko",
#         "Chinese (Simplified)": "zh-cn",
#         "Arabic": "ar",
#         "Hindi": "hi",
#         "Dutch": "nl",
#         "Swedish": "sv",
#         "Turkish": "tr",
#         "Polish": "pl",
#         "Greek": "el"
#     }
#     language_display = {
#         "Spanish": "🇪🇸 Spanish",
#         "French": "🇫🇷 French",
#         "German": "🇩🇪 German",
#         "Italian": "🇮🇹 Italian",
#         "Portuguese": "🇵🇹 Portuguese",
#         "Russian": "🇷🇺 Russian",
#         "Japanese": "🇯🇵 Japanese",
#         "Korean": "🇰🇷 Korean",
#         "Chinese (Simplified)": "🇨🇳 Chinese",
#         "Arabic": "🇦🇪 Arabic",
#         "Hindi": "🇮🇳 Hindi",
#         "Dutch": "🇳🇱 Dutch",
#         "Swedish": "🇸🇪 Swedish",
#         "Turkish": "🇹🇷 Turkish",
#         "Polish": "🇵🇱 Polish",
#         "Greek": "🇬🇷 Greek"
#     }
#     selected_language = st.selectbox(
#         "Select language to translate to:",
#         list(languages.keys()),
#         format_func=lambda x: language_display[x]
#     )
#     return selected_language, languages[selected_language]

# def record_audio():
#     """Record audio from microphone"""
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         st.session_state.status_placeholder.markdown('<p class="status-recording">● Recording in progress - Speak now...</p>', unsafe_allow_html=True)
#         recognizer.adjust_for_ambient_noise(source, duration=0.5)
#         audio = recognizer.listen(source, timeout=10, phrase_time_limit=7)
#         return audio.get_wav_data()

# def render_dashboard(selected_language, language_code):
#     """Render the main translation dashboard"""
#     if 'status_placeholder' not in st.session_state:
#         st.session_state.status_placeholder = st.empty()
    
#     # Display status indicator area
#     st.session_state.status_placeholder.markdown('<p>Ready to record</p>', unsafe_allow_html=True)
    
#     # Recording button
#     if st.button("🎙️ Record & Translate", use_container_width=True):
#         start_time = time.time()
#         try:
#             # Record audio
#             audio_data = record_audio()
            
#             # Update status
#             st.session_state.status_placeholder.markdown('<p class="status-processing">⚙️ Transcribing audio with Vosk...</p>', unsafe_allow_html=True)
            
#             # Transcribe with Vosk
#             transcription = transcribe_audio_with_vosk(audio_data)
            
#             # Update status
#             st.session_state.status_placeholder.markdown('<p class="status-processing">⚙️ Translating text...</p>', unsafe_allow_html=True)
            
#             # Translate text
#             translator = GoogleTranslator(source='auto', target=language_code)
#             translation = translator.translate(transcription)
            
#             # Update status
#             st.session_state.status_placeholder.markdown('<p class="status-processing">⚙️ Enhancing translation...</p>', unsafe_allow_html=True)
            
#             # Enhance translation with basic NLP
#             enhanced_translation = enhance_translation(translation, selected_language)
            
#             # Generate audio for translation
#             audio_bytes = BytesIO()
#             tts = gTTS(text=enhanced_translation, lang=language_code)
#             tts.write_to_fp(audio_bytes)
#             audio_bytes.seek(0)
            
#             # Calculate processing time
#             end_time = time.time()
#             processing_time = end_time - start_time
#             st.session_state.processing_time = processing_time
            
#             # Increment translation count
#             st.session_state.translation_count += 1
            
#             # Create translation result object
#             translation_id = str(uuid.uuid4())[:8]
#             translation_result = {
#                 "id": translation_id,
#                 "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
#                 "source_language": "Auto-detected",
#                 "target_language": selected_language,
#                 "original_text": transcription,
#                 "translated_text": enhanced_translation,
#                 "audio_bytes": audio_bytes.getvalue(),
#                 "processing_time": processing_time
#             }
            
#             # Add to history (limit to 10 items)
#             st.session_state.history.insert(0, translation_result)
#             if len(st.session_state.history) > 10:
#                 st.session_state.history.pop()
            
#             # Update status
#             st.session_state.status_placeholder.markdown('<p class="status-success">✅ Translation complete!</p>', unsafe_allow_html=True)
            
#             # Force page to update with new results
#             st.experimental_rerun()
        
#         except Exception as e:
#             st.session_state.status_placeholder.empty()
#             st.markdown(f'<div class="error-notification">❌ Error: {str(e)}</div>', unsafe_allow_html=True)
#             st.markdown('<div class="info-notification">ℹ️ Try again or check if your microphone is working properly.</div>', unsafe_allow_html=True)

# def render_results():
#     """Render translation results and history"""
#     if st.session_state.history:
#         # Latest translation
#         latest = st.session_state.history[0]
        
#         # Display result in a container
#         st.markdown('<div class="custom-container">', unsafe_allow_html=True)
        
#         # Display metrics
#         col1, col2, col3 = st.columns(3)
#         with col1:
#             st.markdown('<div class="metric-container">', unsafe_allow_html=True)
#             st.markdown(f'<p class="metric-value">{st.session_state.translation_count}</p>', unsafe_allow_html=True)
#             st.markdown('<p class="metric-label">Translations</p>', unsafe_allow_html=True)
#             st.markdown('</div>', unsafe_allow_html=True)
        
#         with col2:
#             st.markdown('<div class="metric-container">', unsafe_allow_html=True)
#             st.markdown(f'<p class="metric-value">{latest["processing_time"]:.1f}s</p>', unsafe_allow_html=True)
#             st.markdown('<p class="metric-label">Processing Time</p>', unsafe_allow_html=True)
#             st.markdown('</div>', unsafe_allow_html=True)
        
#         with col3:
#             st.markdown('<div class="metric-container">', unsafe_allow_html=True)
#             st.markdown(f'<p class="metric-value">{len(latest["original_text"].split())}</p>', unsafe_allow_html=True)
#             st.markdown('<p class="metric-label">Words Translated</p>', unsafe_allow_html=True)
#             st.markdown('</div>', unsafe_allow_html=True)
        
#         # Display latest result
#         st.markdown('<h3 style="margin-top:20px; color: #e0e0e0;">Latest Translation</h3>', unsafe_allow_html=True)
        
#         # Audio player
#         st.markdown('<p style="font-weight:600; margin-bottom:5px; color: #e0e0e0;">🔊 Listen to translation:</p>', unsafe_allow_html=True)
#         st.markdown(get_audio_player_html(latest["audio_bytes"]), unsafe_allow_html=True)
        
#         # Original text
#         st.markdown('<div class="result-box">', unsafe_allow_html=True)
#         st.markdown('<p class="result-box-header">🗣️ Original Text:</p>', unsafe_allow_html=True)
#         st.markdown(f'<p class="result-text">{latest["original_text"]}</p>', unsafe_allow_html=True)
#         st.markdown('</div>', unsafe_allow_html=True)
        
#         # Translated text
#         st.markdown('<div class="result-box">', unsafe_allow_html=True)
#         st.markdown(f'<p class="result-box-header">🌍 Translated Text ({latest["target_language"]}):</p>', unsafe_allow_html=True)
#         st.markdown(f'<p class="result-text">{latest["translated_text"]}</p>', unsafe_allow_html=True)
#         st.markdown('</div>', unsafe_allow_html=True)
        
#         st.markdown('</div>', unsafe_allow_html=True)
        
#         # Show history in tabs
#         if len(st.session_state.history) > 1:
#             st.markdown('<h3 style="margin-top:20px; color: #e0e0e0;">Translation History</h3>', unsafe_allow_html=True)
#             tabs = st.tabs([f"#{i+1}: {h['target_language']}" for i, h in enumerate(st.session_state.history[1:])])
            
#             for i, tab in enumerate(tabs):
#                 with tab:
#                     hist_item = st.session_state.history[i+1]
                    
#                     # Original text
#                     st.markdown('<div class="result-box">', unsafe_allow_html=True)
#                     st.markdown('<p class="result-box-header">🗣️ Original Text:</p>', unsafe_allow_html=True)
#                     st.markdown(f'<p class="result-text">{hist_item["original_text"]}</p>', unsafe_allow_html=True)
#                     st.markdown('</div>', unsafe_allow_html=True)
                    
#                     # Translated text
#                     st.markdown('<div class="result-box">', unsafe_allow_html=True)
#                     st.markdown(f'<p class="result-box-header">🌍 Translated Text ({hist_item["target_language"]}):</p>', unsafe_allow_html=True)
#                     st.markdown(f'<p class="result-text">{hist_item["translated_text"]}</p>', unsafe_allow_html=True)
#                     st.markdown('</div>', unsafe_allow_html=True)
                    
#                     # Audio player
#                     st.markdown('<p style="font-weight:600; margin-bottom:5px; color: #e0e0e0;">🔊 Listen to translation:</p>', unsafe_allow_html=True)
#                     st.markdown(get_audio_player_html(hist_item["audio_bytes"]), unsafe_allow_html=True)
                    
#                     st.markdown(f"<p style='color:#a0a0a0; font-size:14px;'>Processed on {hist_item['timestamp']} (took {hist_item['processing_time']:.1f}s)</p>", unsafe_allow_html=True)

# def render_footer():
#     """Render page footer"""
#     st.markdown('<div class="footer">', unsafe_allow_html=True)
#     st.markdown('🚀 Real-Time Speech Translator • Powered by Vosk & Google Translate', unsafe_allow_html=True)
#     st.markdown('</div>', unsafe_allow_html=True)

# # ---------------------- Main Application ----------------------
# def main():
#     render_header()
    
#     # Main content in two columns
#     col1, col2 = st.columns([1, 2])
    
#     with col1:
#         st.markdown('<div class="custom-container">', unsafe_allow_html=True)
#         selected_language, language_code = render_language_selector()
        
#         # Advanced options
#         with st.expander("⚙️ Advanced Options"):
#             st.checkbox("Use offline speech recognition", value=True, disabled=True, 
#                        help="Uses Vosk for offline speech recognition")
#             st.checkbox("Enhance translation quality", value=True, disabled=True, 
#                        help="Uses basic NLP to improve translation quality")
#             st.checkbox("Auto-detect source language", value=True, disabled=True, 
#                        help="Automatically detects the spoken language")
        
#         # Main translation dashboard
#         render_dashboard(selected_language, language_code)
        
#         # Help section
#         with st.expander("ℹ️ How to use"):
#             st.markdown("""
#             1. Select your target language from the dropdown
#             2. Click the "Record & Translate" button
#             3. Speak clearly for up to 7 seconds
#             4. Wait for processing to complete
#             5. View and listen to your translation
            
#             **Note:** The first translation may take longer as the speech recognition model needs to be downloaded.
#             """)
        
#         st.markdown('</div>', unsafe_allow_html=True)
    
#     with col2:
#         render_results()
    
#     # First-time setup notice
#     if not st.session_state.model_loaded and not st.session_state.history:
#         st.markdown('<div class="info-notification">', unsafe_allow_html=True)
#         st.markdown('ℹ️ **First-time setup**')
#         st.markdown("""
#         The first time you use the translator, a speech recognition model (~50MB) will be downloaded.
#         This may take a few minutes but only happens once. After that, translations will be much faster.
#         """, unsafe_allow_html=True)
#         st.markdown('</div>', unsafe_allow_html=True)
    
#     render_footer()

# if __name__ == "__main__":
#     main()












import streamlit as st
import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
import base64
import os
import tempfile
import time
from io import BytesIO
import uuid
import nltk
from nltk.tokenize import sent_tokenize
import string
import json
import vosk
import wave
import numpy as np
import requests
from tqdm import tqdm
import zipfile
import subprocess

# Download NLTK data (only needed first time)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# ---------------------- Page Configuration ----------------------
st.set_page_config(
    page_title="Real-Time Speech Translator",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------- Custom CSS for Dark Mode UI ----------------------
st.markdown("""
<style>
/* Main container styling */
.main {
    background-color: #121212;
    color: #e0e0e0;
}

/* Custom container */
.custom-container {
    background-color: #1e1e1e;
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    margin-bottom: 24px;
    border: 1px solid #333;
}

/* Header styling */
.main-header {
    font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
    font-weight: 800;
    font-size: 42px;
    margin-bottom: 0;
    text-align: center;
    background: linear-gradient(90deg, #4776E6 0%, #8E54E9 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    padding: 10px 0;
}

.subtitle {
    font-size: 18px;
    color: #a0a0a0;
    text-align: center;
    margin-bottom: 20px;
}

/* Recording button */
.stButton > button {
    width: 100%;
    background: linear-gradient(90deg, #4776E6 0%, #8E54E9 100%);
    color: white;
    font-weight: bold;
    font-size: 18px;
    padding: 15px 0;
    border: none;
    border-radius: 8px;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #3A67D7 0%, #7F45DA 100%);
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(71, 118, 230, 0.5);
}

/* Status indicators */
.status-recording {
    color: #ff4d4d;
    font-weight: bold;
    animation: pulse 1.5s infinite;
}

.status-processing {
    color: #ffa64d;
    font-weight: bold;
}

.status-success {
    color: #4dff4d;
    font-weight: bold;
}

/* Results containers */
.result-box {
    background-color: #252525;
    border-radius: 8px;
    padding: 20px;
    border-left: 5px solid #4776E6;
    margin-bottom: 15px;
}

.result-box-header {
    font-weight: bold;
    color: #4776E6;
    margin-bottom: 10px;
    font-size: 18px;
}

.result-text {
    line-height: 1.6;
    font-size: 16px;
    color: #e0e0e0;
}

/* Language selector */
.language-header {
    font-weight: 600;
    color: #a0a0a0;
    margin-bottom: 8px;
}

/* API Selector */
.api-selector {
    background-color: #252525;
    padding: 16px;
    border-radius: 12px;
    margin-bottom: 15px;
    border: 1px solid #333;
}

/* Audio player */
audio {
    width: 100%;
    border-radius: 30px;
    background-color: #333;
}

/* Metrics */
.metric-container {
    background-color: #252525;
    border-radius: 12px;
    padding: 15px;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    border: 1px solid #333;
}

.metric-value {
    font-size: 24px;
    font-weight: bold;
    color: #4776E6;
}

.metric-label {
    font-size: 14px;
    color: #a0a0a0;
}

/* Animation */
@keyframes pulse {
    0% { opacity: 1; }
    50% { opacity: 0.5; }
    100% { opacity: 1; }
}

/* Footer */
.footer {
    text-align: center;
    color: #a0a0a0;
    font-size: 14px;
    margin-top: 30px;
    padding-top: 10px;
    border-top: 1px solid #333;
}

/* Error notification */
.error-notification {
    background-color: #330000;
    border-left: 5px solid #ff4d4d;
    padding: 15px;
    border-radius: 8px;
    margin-bottom: 20px;
    color: #ff9999;
}

/* Success notification */
.success-notification {
    background-color: #003300;
    border-left: 5px solid #4dff4d;
    padding: 15px;
    border-radius: 8px;
    margin-bottom: 20px;
    color: #99ff99;
}

/* Info notification */
.info-notification {
    background-color: #000033;
    border-left: 5px solid #4d4dff;
    padding: 15px;
    border-radius: 8px;
    margin-bottom: 20px;
    color: #9999ff;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background-color: #1e1e1e;
    border-radius: 8px;
    padding: 5px;
}

.stTabs [data-baseweb="tab"] {
    height: 50px;
    border-radius: 6px;
    padding: 0 20px;
    background-color: #252525;
    color: #e0e0e0;
}

.stTabs [aria-selected="true"] {
    background-color: #4776E6 !important;
    color: white !important;
}

/* Text inputs */
div[data-baseweb="input"] {
    background-color: #252525 !important;
    border: 1px solid #333 !important;
    border-radius: 8px !important;
}

div[data-baseweb="input"] input {
    color: #e0e0e0 !important;
}

/* Select boxes */
div[data-baseweb="select"] {
    background-color: #252525 !important;
    border: 1px solid #333 !important;
    border-radius: 8px !important;
}

div[data-baseweb="select"] div[data-testid="stMarkdownContainer"] {
    color: #e0e0e0 !important;
}

/* Checkbox */
.stCheckbox label {
    color: #e0e0e0 !important;
}

/* Expander */
.streamlit-expanderHeader {
    background-color: #252525 !important;
    color: #e0e0e0 !important;
    border-radius: 8px !important;
}

.streamlit-expanderContent {
    background-color: #1e1e1e !important;
    color: #e0e0e0 !important;
    border-radius: 0 0 8px 8px !important;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 10px;
    height: 10px;
}

::-webkit-scrollbar-track {
    background: #1e1e1e;
}

::-webkit-scrollbar-thumb {
    background: #4776E6;
    border-radius: 5px;
}

::-webkit-scrollbar-thumb:hover {
    background: #8E54E9;
}
</style>
""", unsafe_allow_html=True)

# Helper function to get audio playback HTML
def get_audio_player_html(audio_bytes):
    """Generate HTML for audio player with custom styling"""
    b64 = base64.b64encode(audio_bytes).decode()
    return f"""
    <audio controls autoplay="true">
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    """

# ---------------------- Initialize Session State ----------------------
if 'history' not in st.session_state:
    st.session_state.history = []
if 'processing_time' not in st.session_state:
    st.session_state.processing_time = 0
if 'translation_count' not in st.session_state:
    st.session_state.translation_count = 0
if 'vosk_model' not in st.session_state:
    st.session_state.vosk_model = None
if 'model_loaded' not in st.session_state:
    st.session_state.model_loaded = False

# ---------------------- Utility Functions ----------------------
def check_ffmpeg():
    """Check if ffmpeg is installed"""
    try:
        subprocess.run(['ffmpeg', '-version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except:
        return False

# ---------------------- Vosk Model Download ----------------------
def download_vosk_model():
    """Download and initialize Vosk model for offline speech recognition"""
    try:
        # Create models directory if it doesn't exist
        if not os.path.exists("models"):
            os.makedirs("models")
        
        # Check if model already exists
        if os.path.exists("models/vosk-model-small-en-us-0.15"):
            st.session_state.model_loaded = True
            return True
        
        # URL for small English model
        model_url = "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip"
        zip_path = "models/vosk-model-small-en-us-0.15.zip"
        
        # Download the model
        with st.spinner("Downloading speech recognition model (this may take a few minutes)..."):
            response = requests.get(model_url, stream=True)
            total_size = int(response.headers.get('content-length', 0))
            
            with open(zip_path, 'wb') as file, tqdm(
                desc="Downloading model",
                total=total_size,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
            ) as bar:
                for data in response.iter_content(chunk_size=1024):
                    size = file.write(data)
                    bar.update(size)
        
        # Extract the model
        with st.spinner("Extracting model..."):
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall("models/")
            
            # Remove the zip file to save space
            os.remove(zip_path)
        
        st.session_state.model_loaded = True
        return True
    
    except Exception as e:
        st.error(f"Error downloading model: {str(e)}")
        return False

def transcribe_audio_with_vosk(audio_data):
    """Transcribe audio using Vosk (offline speech recognition)"""
    try:
        if not st.session_state.model_loaded:
            success = download_vosk_model()
            if not success:
                return "Error loading speech recognition model."
        
        # Initialize Vosk model if not already done
        if st.session_state.vosk_model is None:
            from vosk import Model, KaldiRecognizer
            model_path = "models/vosk-model-small-en-us-0.15"
            st.session_state.vosk_model = Model(model_path)
        
        # Create a temporary WAV file
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_wav:
            temp_wav_path = temp_wav.name
            temp_wav.write(audio_data)
        
        # Process with Vosk
        wf = wave.open(temp_wav_path, "rb")
        
        # Check if audio format is compatible
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
            # Convert to compatible format if needed
            if check_ffmpeg():
                output_path = temp_wav_path + "_converted.wav"
                subprocess.run(['ffmpeg', '-i', temp_wav_path, '-acodec', 'pcm_s16le', '-ac', '1', '-ar', '16000', output_path], 
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                wf.close()
                wf = wave.open(output_path, "rb")
            else:
                st.warning("Audio format conversion required but ffmpeg is not installed. Results may be inaccurate.")
        
        # Create recognizer
        from vosk import KaldiRecognizer
        rec = KaldiRecognizer(st.session_state.vosk_model, wf.getframerate())
        rec.SetWords(True)
        
        results = []
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                part_result = json.loads(rec.Result())
                results.append(part_result.get('text', ''))
        
        part_result = json.loads(rec.FinalResult())
        results.append(part_result.get('text', ''))
        
        # Clean up temporary files
        wf.close()
        os.unlink(temp_wav_path)
        if os.path.exists(temp_wav_path + "_converted.wav"):
            os.unlink(temp_wav_path + "_converted.wav")
        
        return " ".join(results).strip()
    
    except Exception as e:
        return f"Error in speech recognition: {str(e)}"

def enhance_translation(text, target_language):
    """Enhance translation using basic NLP techniques (free alternative to Cohere)"""
    # Split into sentences
    sentences = sent_tokenize(text)
    
    # Basic enhancements
    enhanced_sentences = []
    for sentence in sentences:
        # Capitalize first letter of each sentence
        if sentence and len(sentence) > 0:
            sentence = sentence[0].upper() + sentence[1:]
        
                # Ensure proper punctuation
        if sentence and len(sentence) > 0 and sentence[-1] not in string.punctuation:
            sentence += '.'
        
        # Add to enhanced sentences
        enhanced_sentences.append(sentence)
    
    # Join sentences with proper spacing
    enhanced_text = ' '.join(enhanced_sentences)
    
    # Remove double spaces
    enhanced_text = ' '.join(enhanced_text.split())
    
    return enhanced_text

# ---------------------- UI Components ----------------------
def render_header():
    """Render the application header"""
    st.markdown('<h1 class="main-header">Real-Time Speech Translator 🎙️</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Powered by Vosk & Google Translate - Free & Offline Speech Translation</p>', unsafe_allow_html=True)

def render_language_selector():
    """Render language selection interface"""
    st.markdown('<p class="language-header">🌍 Target Language</p>', unsafe_allow_html=True)
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
        "Hindi": "hi",
        "Dutch": "nl",
        "Swedish": "sv",
        "Turkish": "tr",
        "Polish": "pl",
        "Greek": "el"
    }
    language_display = {
        "Spanish": "🇪🇸 Spanish",
        "French": "🇫🇷 French",
        "German": "🇩🇪 German",
        "Italian": "🇮🇹 Italian",
        "Portuguese": "🇵🇹 Portuguese",
        "Russian": "🇷🇺 Russian",
        "Japanese": "🇯🇵 Japanese",
        "Korean": "🇰🇷 Korean",
        "Chinese (Simplified)": "🇨🇳 Chinese",
        "Arabic": "🇦🇪 Arabic",
        "Hindi": "🇮🇳 Hindi",
        "Dutch": "🇳🇱 Dutch",
        "Swedish": "🇸🇪 Swedish",
        "Turkish": "🇹🇷 Turkish",
        "Polish": "🇵🇱 Polish",
        "Greek": "🇬🇷 Greek"
    }
    selected_language = st.selectbox(
        "Select language to translate to:",
        list(languages.keys()),
        format_func=lambda x: language_display[x]
    )
    return selected_language, languages[selected_language]

def record_audio():
    """Record audio from microphone"""
    try:
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.session_state.status_placeholder.markdown('<p class="status-recording">● Recording in progress - Speak now...</p>', unsafe_allow_html=True)
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=7)
            return audio.get_wav_data()
    except sr.RequestError:
        raise Exception("API unavailable. Check your internet connection.")
    except sr.WaitTimeoutError:
        raise Exception("No speech detected. Please try again and speak clearly.")
    except sr.UnknownValueError:
        raise Exception("Could not understand audio. Please try again.")
    except Exception as e:
        if "microphone" in str(e).lower():
            raise Exception("Microphone not accessible. Please check your microphone settings.")
        else:
            raise e

def render_dashboard(selected_language, language_code):
    """Render the main translation dashboard"""
    if 'status_placeholder' not in st.session_state:
        st.session_state.status_placeholder = st.empty()
    
    # Display status indicator area
    st.session_state.status_placeholder.markdown('<p>Ready to record</p>', unsafe_allow_html=True)
    
    # Recording button
    if st.button("🎙️ Record & Translate", use_container_width=True):
        start_time = time.time()
        try:
            # Record audio
            audio_data = record_audio()
            
            # Update status
            st.session_state.status_placeholder.markdown('<p class="status-processing">⚙️ Transcribing audio with Vosk...</p>', unsafe_allow_html=True)
            
            # Transcribe with Vosk
            transcription = transcribe_audio_with_vosk(audio_data)
            
            # Update status
            st.session_state.status_placeholder.markdown('<p class="status-processing">⚙️ Translating text...</p>', unsafe_allow_html=True)
            
            # Translate text
            translator = GoogleTranslator(source='auto', target=language_code)
            translation = translator.translate(transcription)
            
            # Update status
            st.session_state.status_placeholder.markdown('<p class="status-processing">⚙️ Enhancing translation...</p>', unsafe_allow_html=True)
            
            # Enhance translation with basic NLP
            enhanced_translation = enhance_translation(translation, selected_language)
            
            # Generate audio for translation
            audio_bytes = BytesIO()
            tts = gTTS(text=enhanced_translation, lang=language_code)
            tts.write_to_fp(audio_bytes)
            audio_bytes.seek(0)
            
            # Calculate processing time
            end_time = time.time()
            processing_time = end_time - start_time
            st.session_state.processing_time = processing_time
            
            # Increment translation count
            st.session_state.translation_count += 1
            
            # Create translation result object
            translation_id = str(uuid.uuid4())[:8]
            translation_result = {
                "id": translation_id,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "source_language": "Auto-detected",
                "target_language": selected_language,
                "original_text": transcription,
                "translated_text": enhanced_translation,
                "audio_bytes": audio_bytes.getvalue(),
                "processing_time": processing_time
            }
            
            # Add to history (limit to 10 items)
            st.session_state.history.insert(0, translation_result)
            if len(st.session_state.history) > 10:
                st.session_state.history.pop()
            
            # Update status
            st.session_state.status_placeholder.markdown('<p class="status-success">✅ Translation complete!</p>', unsafe_allow_html=True)
            
            # Force page to update with new results
            try:
                st.rerun()
            except:
                # Fallback for older Streamlit versions
                st.experimental_rerun()
        
        except Exception as e:
            st.session_state.status_placeholder.empty()
            st.markdown(f'<div class="error-notification">❌ Error: {str(e)}</div>', unsafe_allow_html=True)
            st.markdown('<div class="info-notification">ℹ️ Try again or check if your microphone is working properly.</div>', unsafe_allow_html=True)

def render_results():
    """Render translation results and history"""
    if st.session_state.history:
        # Latest translation
        latest = st.session_state.history[0]
        
        # Display result in a container
        st.markdown('<div class="custom-container">', unsafe_allow_html=True)
        
        # Display metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown('<div class="metric-container">', unsafe_allow_html=True)
            st.markdown(f'<p class="metric-value">{st.session_state.translation_count}</p>', unsafe_allow_html=True)
            st.markdown('<p class="metric-label">Translations</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-container">', unsafe_allow_html=True)
            st.markdown(f'<p class="metric-value">{latest["processing_time"]:.1f}s</p>', unsafe_allow_html=True)
            st.markdown('<p class="metric-label">Processing Time</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="metric-container">', unsafe_allow_html=True)
            st.markdown(f'<p class="metric-value">{len(latest["original_text"].split())}</p>', unsafe_allow_html=True)
            st.markdown('<p class="metric-label">Words Translated</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Display latest result
        st.markdown('<h3 style="margin-top:20px; color: #e0e0e0;">Latest Translation</h3>', unsafe_allow_html=True)
        
        # Audio player
        st.markdown('<p style="font-weight:600; margin-bottom:5px; color: #e0e0e0;">🔊 Listen to translation:</p>', unsafe_allow_html=True)
        st.markdown(get_audio_player_html(latest["audio_bytes"]), unsafe_allow_html=True)
        
        # Original text
        st.markdown('<div class="result-box">', unsafe_allow_html=True)
        st.markdown('<p class="result-box-header">🗣️ Original Text:</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="result-text">{latest["original_text"]}</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Translated text
        st.markdown('<div class="result-box">', unsafe_allow_html=True)
        st.markdown(f'<p class="result-box-header">🌍 Translated Text ({latest["target_language"]}):</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="result-text">{latest["translated_text"]}</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Show history in tabs
        if len(st.session_state.history) > 1:
            st.markdown('<h3 style="margin-top:20px; color: #e0e0e0;">Translation History</h3>', unsafe_allow_html=True)
            tabs = st.tabs([f"#{i+1}: {h['target_language']}" for i, h in enumerate(st.session_state.history[1:])])
            
            for i, tab in enumerate(tabs):
                with tab:
                    hist_item = st.session_state.history[i+1]
                    
                    # Original text
                    st.markdown('<div class="result-box">', unsafe_allow_html=True)
                    st.markdown('<p class="result-box-header">🗣️ Original Text:</p>', unsafe_allow_html=True)
                    st.markdown(f'<p class="result-text">{hist_item["original_text"]}</p>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Translated text
                    st.markdown('<div class="result-box">', unsafe_allow_html=True)
                    st.markdown(f'<p class="result-box-header">🌍 Translated Text ({hist_item["target_language"]}):</p>', unsafe_allow_html=True)
                    st.markdown(f'<p class="result-text">{hist_item["translated_text"]}</p>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Audio player
                    st.markdown('<p style="font-weight:600; margin-bottom:5px; color: #e0e0e0;">🔊 Listen to translation:</p>', unsafe_allow_html=True)
                    st.markdown(get_audio_player_html(hist_item["audio_bytes"]), unsafe_allow_html=True)
                    
                    st.markdown(f"<p style='color:#a0a0a0; font-size:14px;'>Processed on {hist_item['timestamp']} (took {hist_item['processing_time']:.1f}s)</p>", unsafe_allow_html=True)

def render_footer():
    """Render page footer"""
    st.markdown('<div class="footer">', unsafe_allow_html=True)
    st.markdown('🚀 Real-Time Speech Translator • Powered by Vosk & Google Translate', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------- Main Application ----------------------
def main():
    render_header()
    
    # Main content in two columns
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown('<div class="custom-container">', unsafe_allow_html=True)
        selected_language, language_code = render_language_selector()
        
        # Advanced options
        with st.expander("⚙️ Advanced Options"):
            st.checkbox("Use offline speech recognition", value=True, disabled=True, 
                       help="Uses Vosk for offline speech recognition")
            st.checkbox("Enhance translation quality", value=True, disabled=True, 
                       help="Uses basic NLP to improve translation quality")
            st.checkbox("Auto-detect source language", value=True, disabled=True, 
                       help="Automatically detects the spoken language")
        
        # Main translation dashboard
        render_dashboard(selected_language, language_code)
        
        # Help section
        with st.expander("ℹ️ How to use"):
            st.markdown("""
            1. Select your target language from the dropdown
            2. Click the "Record & Translate" button
            3. Speak clearly for up to 7 seconds
            4. Wait for processing to complete
            5. View and listen to your translation
            
            **Note:** The first translation may take longer as the speech recognition model needs to be downloaded.
            """)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        render_results()
    
    # First-time setup notice
    if not st.session_state.model_loaded and not st.session_state.history:
        st.markdown('<div class="info-notification">', unsafe_allow_html=True)
        st.markdown('ℹ️ **First-time setup**')
        st.markdown("""
        The first time you use the translator, a speech recognition model (~50MB) will be downloaded.
        This may take a few minutes but only happens once. After that, translations will be much faster.
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    render_footer()

if __name__ == "__main__":
    main()


