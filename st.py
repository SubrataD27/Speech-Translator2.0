# import streamlit as st
# import cohere
# import openai
# import speech_recognition as sr
# from googletrans import Translator
# from gtts import gTTS
# import base64
# import os
# import tempfile

# # ---------------------- API KEYS ----------------------
# COHERE_API_KEY = "7Q0czs2CFyxLxwOMcRH97CR8OniUrQ1LbgRF7uw1"
# OPENAI_API_KEY = "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"

# co = cohere.Client(COHERE_API_KEY)
# openai.api_key = OPENAI_API_KEY

# # ---------------------- Streamlit UI ----------------------
# st.set_page_config(page_title="AI Speech Translator", page_icon="🎙️", layout="centered")
# st.title("🎙️ AI-Powered Speech Translator")
# st.markdown("Speak in any language & get instant translations!")

# # ---------------------- Language Selection ----------------------
# languages = {
#     "Spanish": "es", "French": "fr", "German": "de", "Italian": "it",
#     "Portuguese": "pt", "Russian": "ru", "Japanese": "ja", "Korean": "ko",
#     "Chinese (Simplified)": "zh-cn", "Arabic": "ar", "Hindi": "hi"
# }
# selected_language = st.selectbox("🌍 Select Target Language:", list(languages.keys()))
# target_language_code = languages[selected_language]

# # ---------------------- Recording & AI Speech Recognition ----------------------
# if st.button("🎙️ Record & Translate"):
#     try:
#         with st.spinner("🎤 Recording... Speak now!"):
#             recognizer = sr.Recognizer()
#             with sr.Microphone() as source:
#                 recognizer.adjust_for_ambient_noise(source, duration=1)
#                 audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)

#         with st.spinner("🔄 Transcribing with AI..."):
#             audio_data = audio.get_wav_data()
#             response = openai.Audio.transcribe("whisper-1", audio_data)
#             text = response["text"]

#         with st.spinner("🌍 Translating..."):
#             translator = Translator()
#             translation = translator.translate(text, dest=target_language_code)

#         # AI-Powered Refinement (Cohere)
#         with st.spinner("🧠 Enhancing translation..."):
#             refined_translation = co.generate(
#                 model="command-xlarge",
#                 prompt=f"Refine this translation for better clarity: {translation.text}",
#                 max_tokens=100
#             ).generations[0].text

#         # Generate Speech from Translation
#         with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
#             tts = gTTS(text=refined_translation, lang=target_language_code)
#             tts.save(temp_audio.name)

#             with open(temp_audio.name, "rb") as f:
#                 audio_bytes = f.read()
#             audio_base64 = base64.b64encode(audio_bytes).decode()
        
#         os.unlink(temp_audio.name)

#         # Display Results
#         st.success("✅ Translation Complete!")
#         st.markdown(f"🗣️ **Original Speech:** {text}")
#         st.markdown(f"🌍 **Translated:** {refined_translation}")
#         st.markdown("🎧 **Listen to Translation:**")
#         st.markdown(f'<audio controls autoplay><source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3"></audio>', unsafe_allow_html=True)

#     except Exception as e:
#         st.error(f"❌ Error: {str(e)}")

# st.markdown("---")
# st.markdown("🚀 Built with **Cohere AI, OpenAI Whisper, and Google Translate**")









import streamlit as st
import cohere
import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
import base64
import os
import tempfile
import time
from io import BytesIO
import uuid
import google.cloud.speech as speech
from google.oauth2 import service_account
import json

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

if 'api_keys_valid' not in st.session_state:
    st.session_state.api_keys_valid = False

if 'processing_time' not in st.session_state:
    st.session_state.processing_time = 0
    
if 'translation_count' not in st.session_state:
    st.session_state.translation_count = 0

if 'api_error' not in st.session_state:
    st.session_state.api_error = None

def validate_api_keys(cohere_key, google_credentials_json):
    """Validate API keys by making minimal test calls"""
    errors = []
    
    # Validate Cohere API key
    try:
        co = cohere.Client(cohere_key)
        co.generate(prompt="Test", max_tokens=1)
    except Exception as e:
        errors.append(f"Cohere API Error: {str(e)}")
    
    # Validate Google Cloud credentials
    try:
        # Parse credentials JSON
        credentials_dict = json.loads(google_credentials_json)
        credentials = service_account.Credentials.from_service_account_info(credentials_dict)
        
        # Create a test client
        client = speech.SpeechClient(credentials=credentials)
        
        # Make a minimal test request
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="en-US",
        )
        audio = speech.RecognitionAudio(content=b"")
        client.recognize(config=config, audio=audio)
        
    except Exception as e:
        error_msg = str(e)
        errors.append(f"Google Cloud API Error: {error_msg}")
    
    if errors:
        st.session_state.api_error = "\n".join(errors)
        return False
    
    st.session_state.api_error = None
    return True

def transcribe_audio(audio_data, language_code="en-US"):
    """Transcribe audio using Google Cloud Speech-to-Text"""
    try:
        # Load credentials from session state
        credentials_dict = json.loads(st.session_state.google_credentials)
        credentials = service_account.Credentials.from_service_account_info(credentials_dict)
        
        # Create speech client
        client = speech.SpeechClient(credentials=credentials)
        
        # Configure the request
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code=language_code,
            enable_automatic_punctuation=True,
        )
        
        # Create an audio object
        audio = speech.RecognitionAudio(content=audio_data)
        
        # Perform the transcription
        response = client.recognize(config=config, audio=audio)
        
        # Extract the transcribed text
        transcript = ""
        for result in response.results:
            transcript += result.alternatives[0].transcript
            
        return transcript
        
    except Exception as e:
        raise Exception(f"Google Speech-to-Text Error: {str(e)}")

def enhance_translation(text, target_language):
    """Use Cohere to enhance translation quality"""
    co = cohere.Client(st.session_state.cohere_api_key)
    response = co.generate(
        model="command-xlarge-nightly",
        prompt=f"""You are an expert translator specializing in natural and fluent translations.
        
Your task is to refine and improve the following machine translation to make it sound more natural and fluent in {target_language}.
Focus on idiomatic expressions, cultural nuances, and natural flow.

Original translation: {text}

Improved translation:""",
        max_tokens=150,
        temperature=0.7,
        k=0,
        stop_sequences=[],
        return_likelihoods="NONE"
    )
    
    refined_text = response.generations[0].text.strip()
    return refined_text

# ---------------------- UI Components ----------------------
def render_header():
    """Render the application header"""
    st.markdown('<h1 class="main-header">Real-Time Speech Translator 🎙️</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Powered by Google Cloud Speech-to-Text & Cohere AI - Translate speech in real-time</p>', unsafe_allow_html=True)

def render_api_config():
    """Render API configuration section"""
    with st.expander("🔑 Configure API Keys", expanded=not st.session_state.api_keys_valid):
        st.markdown('<div class="api-selector">', unsafe_allow_html=True)
        
        # Cohere API key input
        cohere_key = st.text_input(
            "Cohere API Key", 
            value=st.session_state.get('cohere_api_key', ''),
            type="password",
            help="Get your Cohere API key at cohere.ai"
        )
        
        # Google Cloud credentials input
        st.markdown("##### Google Cloud Credentials")
        st.markdown("Paste your Google Cloud service account JSON credentials:")
        google_credentials = st.text_area(
            "Google Cloud JSON Credentials",
            value=st.session_state.get('google_credentials', ''),
            height=150,
            help="Create a service account key in Google Cloud Console"
        )
        
        if st.button("💾 Save API Keys"):
            if cohere_key and google_credentials:
                with st.spinner("Validating API keys..."):
                    valid = validate_api_keys(cohere_key, google_credentials)
                    if valid:
                        st.session_state.cohere_api_key = cohere_key
                        st.session_state.google_credentials = google_credentials
                        st.session_state.api_keys_valid = True
                        st.success("✅ API keys validated successfully!")
                        time.sleep(1)
                        st.experimental_rerun()
            else:
                st.warning("⚠️ Please enter both API keys")
        
        # Display API error if any
        if st.session_state.api_error:
            for error in st.session_state.api_error.split("\n"):
                st.markdown(f'<div class="error-notification">❌ {error}</div>', unsafe_allow_html=True)
            
            # Help for Google Cloud credentials
            if "Google Cloud" in st.session_state.api_error:
                st.markdown("""
                <div class="info-notification">
                <strong>🔑 Google Cloud Credentials:</strong><br>
                To get valid Google Cloud credentials:
                <ol>
                    <li>Go to <a href="https://console.cloud.google.com/" target="_blank" style="color: #8E54E9;">Google Cloud Console</a></li>
                    <li>Create a new project (or select existing)</li>
                    <li>Enable the Speech-to-Text API in APIs & Services</li>
                    <li>Create a Service Account under IAM & Admin</li>
                    <li>Add the Speech-to-Text Admin role</li>
                    <li>Create and download a JSON key</li>
                    <li>Paste the entire contents of the JSON file here</li>
                </ol>
                </div>
                """, unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True)

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
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.session_state.status_placeholder.markdown('<p class="status-recording">● Recording in progress - Speak now...</p>', unsafe_allow_html=True)
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source, timeout=10, phrase_time_limit=7)
    
    return audio.get_wav_data()

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
            st.session_state.status_placeholder.markdown('<p class="status-processing">⚙️ Transcribing audio with Google Cloud...</p>', unsafe_allow_html=True)
            
            # Transcribe with Google Cloud Speech-to-Text
            transcription = transcribe_audio(audio_data)
            
            # Update status
            st.session_state.status_placeholder.markdown('<p class="status-processing">⚙️ Translating text...</p>', unsafe_allow_html=True)
            
            # Translate text
            translator = GoogleTranslator(source='auto', target=language_code)
            translation = translator.translate(transcription)
            
            # Update status
            st.session_state.status_placeholder.markdown('<p class="status-processing">⚙️ Enhancing translation with Cohere AI...</p>', unsafe_allow_html=True)
            
            # Enhance translation with Cohere
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
    st.markdown('🚀 Real-Time Speech Translator • Powered by Google Cloud Speech-to-Text & Cohere AI', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------- Main Application ----------------------
def main():
    render_header()
    
    # Check if API keys are configured
    if not st.session_state.api_keys_valid:
        render_api_config()
        
        # Show demo notification if API keys not yet validated
        st.markdown('<div class="info-notification">', unsafe_allow_html=True)
        st.markdown('ℹ️ **Configure your API keys to start using the translator**')
        st.markdown("""
        You need to provide valid Cohere API key and Google Cloud credentials to use this app.
        The keys are only stored in your session and are not saved on any server.
        
        <strong>To get Google Cloud credentials:</strong>
        1. Go to the <a href="https://console.cloud.google.com/" target="_blank" style="color: #8E54E9;">Google Cloud Console</a>
        2. Create a project and enable the Speech-to-Text API
        3. Create a service account with Speech-to-Text Admin role
        4. Create and download a JSON key
        5. Paste the entire contents of the JSON file in the configuration section
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Show feature preview
        st.markdown('<h3 style="color: #e0e0e0;">🌟 Features</h3>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<span style="color: #4dff4d;">✅</span> <span style="color: #e0e0e0;"><strong>Advanced voice recognition</strong></span>', unsafe_allow_html=True)
            st.markdown('<span style="color: #4dff4d;">✅</span> <span style="color: #e0e0e0;"><strong>Enhanced translations with AI</strong></span>', unsafe_allow_html=True)
            st.markdown('<span style="color: #4dff4d;">✅</span> <span style="color: #e0e0e0;"><strong>Support for 15+ languages</strong></span>', unsafe_allow_html=True)
        with col2:
            st.markdown('<span style="color: #4dff4d;">✅</span> <span style="color: #e0e0e0;"><strong>Natural-sounding playback</strong></span>', unsafe_allow_html=True)
            st.markdown('<span style="color: #4dff4d;">✅</span> <span <span style="color: #e0e0e0;"><strong>Translation history</strong></span>', unsafe_allow_html=True)
            st.markdown('<span style="color: #4dff4d;">✅</span> <span style="color: #e0e0e0;"><strong>Optimized for accuracy</strong></span>', unsafe_allow_html=True)
    else:
        # Main content in two columns
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown('<div class="custom-container">', unsafe_allow_html=True)
            selected_language, language_code = render_language_selector()
            
            # Advanced options
            with st.expander("⚙️ Advanced Options"):
                st.checkbox("Use Whisper for transcription", value=True, disabled=True, 
                           help="OpenAI Whisper provides superior transcription accuracy")
                st.checkbox("Enhance translation with Cohere", value=True, disabled=True,
                           help="Uses Cohere's AI to improve translation quality")
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
                4. Wait for AI-powered processing to complete
                5. View and listen to your enhanced translation
                """)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col2:
            render_results()
        
        # API Config in expander at the bottom
        render_api_config()
    
    render_footer()

if __name__ == "__main__":
    main()