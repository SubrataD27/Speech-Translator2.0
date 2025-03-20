import streamlit as st
import cohere
import openai
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import base64
import os
import tempfile

# ---------------------- API KEYS ----------------------
COHERE_API_KEY = "7Q0czs2CFyxLxwOMcRH97CR8OniUrQ1LbgRF7uw1"
OPENAI_API_KEY = "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"

co = cohere.Client(COHERE_API_KEY)
openai.api_key = OPENAI_API_KEY

# ---------------------- Streamlit UI ----------------------
st.set_page_config(page_title="AI Speech Translator", page_icon="🎙️", layout="centered")
st.title("🎙️ AI-Powered Speech Translator")
st.markdown("Speak in any language & get instant translations!")

# ---------------------- Language Selection ----------------------
languages = {
    "Spanish": "es", "French": "fr", "German": "de", "Italian": "it",
    "Portuguese": "pt", "Russian": "ru", "Japanese": "ja", "Korean": "ko",
    "Chinese (Simplified)": "zh-cn", "Arabic": "ar", "Hindi": "hi"
}
selected_language = st.selectbox("🌍 Select Target Language:", list(languages.keys()))
target_language_code = languages[selected_language]

# ---------------------- Recording & AI Speech Recognition ----------------------
if st.button("🎙️ Record & Translate"):
    try:
        with st.spinner("🎤 Recording... Speak now!"):
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)

        with st.spinner("🔄 Transcribing with AI..."):
            audio_data = audio.get_wav_data()
            response = openai.Audio.transcribe("whisper-1", audio_data)
            text = response["text"]

        with st.spinner("🌍 Translating..."):
            translator = Translator()
            translation = translator.translate(text, dest=target_language_code)

        # AI-Powered Refinement (Cohere)
        with st.spinner("🧠 Enhancing translation..."):
            refined_translation = co.generate(
                model="command-xlarge",
                prompt=f"Refine this translation for better clarity: {translation.text}",
                max_tokens=100
            ).generations[0].text

        # Generate Speech from Translation
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
            tts = gTTS(text=refined_translation, lang=target_language_code)
            tts.save(temp_audio.name)

            with open(temp_audio.name, "rb") as f:
                audio_bytes = f.read()
            audio_base64 = base64.b64encode(audio_bytes).decode()
        
        os.unlink(temp_audio.name)

        # Display Results
        st.success("✅ Translation Complete!")
        st.markdown(f"🗣️ **Original Speech:** {text}")
        st.markdown(f"🌍 **Translated:** {refined_translation}")
        st.markdown("🎧 **Listen to Translation:**")
        st.markdown(f'<audio controls autoplay><source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3"></audio>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

st.markdown("---")
st.markdown("🚀 Built with **Cohere AI, OpenAI Whisper, and Google Translate**")
