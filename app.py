import streamlit as st
import requests

# Omeife AI API Endpoints
TRANSLATION_API_URL = "https://apis.omeife.ai/api/v1/user/developer/translate"
SPEECH_SYNTHESIS_API_URL = "https://apis.omeife.ai/api/v1/user/translation/speech/query"
API_KEY = "your_api_key_here"  # Replace with your actual API key

# Sample folktales in different languages
folktales = {
    "Igbo": "O once n'ime ugbo ndi Igbo, e nwere tortoise...",
    "Yoruba": "Lọ́dún kan, Ijapa àti Erin jọ sàn...",
    "Hausa": "A wani lokaci, akwai wata kyakkyawar yarinya mai suna...",
    "Nigerian Pidgin": "One time, for one village, tortoise wey sabi trick people...",
    "English": "Once upon a time, in an Igbo village, there was a clever tortoise..."
}

# Function to translate text
def translate_text(text, source_lang, target_lang):
    payload = {
        "text": text,
        "from": source_lang,
        "to": target_lang
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    response = requests.post(TRANSLATION_API_URL, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json().get("translated_text", "Translation failed.")
    return "Error: Translation service unavailable."

# Function to generate speech
def synthesize_speech(text):
    payload = {"question": text}
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    response = requests.post(SPEECH_SYNTHESIS_API_URL, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json().get("audio_url", None)
    return None

# Streamlit UI
st.title("📖 AI-Powered Nigerian Folktale Storytelling")
st.write("Listen to Nigerian folktales in multiple languages!")

# Language selection
language = st.selectbox("Choose a language:", list(folktales.keys()))

# Display selected folktale
story = folktales[language]
st.subheader(f"Folktale in {language}")
st.write(story)

# Translation
target_language = st.selectbox("Translate to:", list(folktales.keys()))
if st.button("Translate"):
    translated_story = translate_text(story, language, target_language)
    st.subheader(f"Translated Story in {target_language}")
    st.write(translated_story)

# Text-to-Speech
if st.button("Listen to Story"):
    audio_url = synthesize_speech(story)
    if audio_url:
        st.audio(audio_url)
    else:
        st.error("Speech synthesis failed. Try again.")

