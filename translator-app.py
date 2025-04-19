#!/usr/bin/env python
# coding: utf-8

# In[22]:


import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import os
import deepl
import pygame
from tempfile import NamedTemporaryFile
from dotenv import load_dotenv


# In[23]:


load_dotenv(dotenv_path= 'C:/Users/aisha/anaconda3/envs/translator-env/.env.txt')


# In[24]:


DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")
translator = deepl.Translator(DEEPL_API_KEY)


# In[28]:


# Configure Streamlit page
st.set_page_config(page_title="Healthcare Translator", layout="centered")
st.title("Healthcare Translation Web App")
st.markdown("**Speak your symptoms. Get real-time translations.**")

# Supported languages
lang_map = {
    "French": "FR",
    "Spanish": "ES",
    "German": "DE",
    "Italian": "IT",
    "Portuguese": "PT-PT",
    "Dutch": "NL"
}
target_lang = st.selectbox("Choose target language", list(lang_map.keys()))

# Initialize pygame for audio playback
pygame.mixer.init()

def record_voice():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        st.info("Listening... Please speak clearly into your microphone.")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            return "Listening timed out. Please try again."

    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand what you said. Please try again."
    except sr.RequestError:
        return "Speech recognition service is unavailable."

def translate_with_deepl(text, target_lang_code):
    try:
        result = translator.translate_text(text, target_lang=target_lang_code)
        return result.text
    except Exception as e:
        return f"DeepL translation error: {str(e)}"

def speak(text, lang_code):
    try:
        tts = gTTS(text=text, lang=lang_code.lower())
        with NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)
            audio_path = fp.name

        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        os.remove(audio_path)
    except Exception as e:
        st.error(f"Speech playback error: {str(e)}")

def run_translation():
    spoken = record_voice()
    st.subheader("Transcript:")
    st.write(spoken)

    if spoken.lower().startswith("sorry") or "error" in spoken.lower():
        st.warning("Voice input was unclear. Please try again.")
        return

    translated = translate_with_deepl(spoken, lang_map[target_lang])
    st.subheader(f"Translation ({target_lang}):")
    st.write(translated)

    if st.button("🔊 Play Translated Audio"):
        speak(translated, lang_map[target_lang])

# Translation trigger button
if st.button("🎤 Record and Translate"):
    with st.spinner("Processing..."):
        run_translation()



