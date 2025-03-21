# 🎙️ Real-time Speech Translator

🚀 **A free & offline speech translation app** using **Vosk & Google Translate**, built with **Streamlit** for an intuitive and sleek user experience.

## ✨ Features

✅ **Offline Speech Recognition** with **Vosk**  
✅ **Translations** powered by **Google Translate**  
✅ **Supports 16 Languages** (Spanish, French, German, Chinese, etc.)  
✅ **Instant Text-to-Speech (TTS)** for translated output  
✅ **Dark Mode UI** with a modern & responsive design  
✅ **Translation History** for quick reference  
✅ **Completely Free** with no API keys required  

## 🔧 Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/speech-translator.git
cd speech-translator
```

### 2️⃣ Install Dependencies
```bash
pip install streamlit speech_recognition deep-translator gtts vosk nltk requests tqdm numpy
```

### 3️⃣ Install FFmpeg (for audio conversion)
- **Windows**: Download from https://ffmpeg.org/download.html and add to PATH
- **macOS**: `brew install ffmpeg`
- **Ubuntu/Debian**: `sudo apt-get install ffmpeg`

### 4️⃣ Run the Application
```bash
streamlit run speech_translator.py
```

## 🖥️ How to Use

1. Select your target language from the dropdown
2. Click the "Record & Translate" button
3. Speak clearly for up to 7 seconds
4. Wait for processing to complete
5. View and listen to your translation

*Note:* The first time you use the translator, a speech recognition model (~50MB) will be downloaded.

## 🛠️ Tech Stack

- **Python**, **Streamlit**
- **Vosk** for offline speech-to-text
- **Google Translate** for language translation
- **gTTS (Google Text-to-Speech)**
- **NLTK** for text enhancement
- **Custom UI Design (CSS for dark theme)**

## 👨‍💻 Developed By

**Subrata** 💙 | Passionate about AI, NLP & Cloud Computing

## 📜 License

This project is licensed under the **MIT License**.
