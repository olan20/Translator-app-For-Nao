#!/usr/bin/env python
# coding: utf-8

# In[22]:


import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import playsound
import os
import deepl
from tempfile import NamedTemporaryFile
from dotenv import load_dotenv


# In[23]:


load_dotenv(dotenv_path= 'C:/Users/aisha/anaconda3/envs/translator-env/.env.txt')


# In[24]:


DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")
translator = deepl.Translator(DEEPL_API_KEY)


# In[25]:


st.set_page_config(page_title="Healthcare Translator", layout="centered")

# Title
st.title("Healthcare Translation Web App")
st.markdown("**Speak your symptoms. Get real-time translations.**")

# Language selection (DeepL supported languages only)
lang_map = {
    "French": "FR",
    "Spanish": "ES",
    "German": "DE",
    "Italian": "IT",
    "Portuguese": "PT-PT",
    "Dutch": "NL"
}
target_lang = st.selectbox("Choose target language", list(lang_map.keys()))


def record_voice():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        st.info("Listening... Please speak into your mic.")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Could not understand audio."


def translate_with_deepl(text, target_lang_code):
    try:
        result = translator.translate_text(text, target_lang=target_lang_code)
        return result.text
    except Exception as e:
        return f"DeepL translation error: {str(e)}"


def speak(text, lang_code):
    try:
        tts = gTTS(text=text, lang=lang_code.lower())
        with NamedTemporaryFile(delete=True, suffix=".mp3") as fp:
            tts.save(fp.name)
            playsound.playsound(fp.name)
    except Exception as e:
        st.error(f"Speech playback error: {str(e)}")


# Main Workflow
if st.button("Record and Translate"):
    with st.spinner("Processing..."):
        spoken = record_voice()
        st.subheader("Transcript:")
        st.write(spoken)

        translated = translate_with_deepl(spoken, lang_map[target_lang])
        st.subheader(f"Translation ({target_lang}):")
        st.write(translated)

        if st.button("Play Translated Audio"):
            speak(translated, lang_map[target_lang])

