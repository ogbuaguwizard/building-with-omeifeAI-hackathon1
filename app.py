import streamlit as st
import pandas as pd
import requests
import json

# Omeife AI API Endpoints
TRANSLATION_API_URL = "https://apis.omeife.ai/api/v1/user/developer/translate"
SPEECH_SYNTHESIS_API_URL = "https://apis.omeife.ai/api/v1/user/translation/speech/query"
API_KEY = "bmxRAdtgcwcCjF9dOmooEIFHZpwGfWG66jqLTkIO57u83Hq4io"

# Load folktales from CSV
@st.cache_data
def load_folktales():
    try:
        return pd.read_csv("folktales.csv", encoding="utf-8", quotechar='"')  # Ensure quotes handle commas
    except Exception as e:
        st.error(f"Error loading folktales: {e}")
        return pd.DataFrame(columns=["title", "origin", "story"])  # Return empty DataFrame on failure

# Function to translate text
def translate_text(text, source_lang, target_lang):
    payload = {"text": text, "from": source_lang, "to": target_lang}
    headers = {"Authorization": f"Bearer {API_KEY}", "Accept": "application/json", "Content-Type": "application/json"}
    
    response = requests.post(TRANSLATION_API_URL, json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json().get("data", {}).get("translated_text", "Translation failed.")
    else:
        return "Translation service unavailable."

# Function to generate speech
def synthesize_speech(text):
    payload = {"question": text}
    headers = {"Authorization": f"Bearer {API_KEY}", "Accept": "application/json", "Content-Type": "application/json"}
    response = requests.post(SPEECH_SYNTHESIS_API_URL, json=payload, headers=headers)
    return response.json().get("audio_url", None) if response.status_code == 200 else None

# Load folktales
folktales_df = load_folktales()

# Streamlit UI
st.title("📖 AI-Powered Nigerian Folktale Storytelling")
st.write("Select a Nigerian folktale, translate it, and listen to it!")

# Select folktale by origin
origins = folktales_df["origin"].unique()
selected_origin = st.selectbox("Choose a folktale origin:", origins)

# Get folktale based on selection
selected_story = folktales_df[folktales_df["origin"] == selected_origin].iloc[0]
st.subheader(f"Story: {selected_story['title']}")
st.write(selected_story["story"])

# Translation
target_language = st.selectbox("Translate to:", ["english", "igbo", "Yoruba", "Hausa", "Pidgin"])
if st.button("Translate"):
    translated_story = translate_text(selected_story["story"], "English", target_language)
    st.subheader(f"Translated Story in {target_language}")
    st.write(translated_story)

# Text-to-Speech
if st.button("Listen to Story"):
    audio_url = synthesize_speech(selected_story["story"])
    if audio_url:
        st.audio(audio_url)
    else:
        st.error("Speech synthesis failed. Try again.")
