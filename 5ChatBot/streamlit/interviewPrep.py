import streamlit as st
import random
import time
import pyttsx3
import speech_recognition as sr
from gtts import gTTS
# import nltk

from bardapi import Bard
import os

st.title("Interview Assistant 🤖")

def text_to_speech(text):
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[1].id)
    rate = engine.getProperty("rate")
    engine.setProperty("rate", 150)
    engine.say(text)
    engine.runAndWait()

def speech_to_text():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Please start speaking...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            print("Recognizing ...")
            text = recognizer.recognize_google(audio, language="en-in")
            return text
        except Exception as e:
            print("Sorry, I didn't understand")
            return "Sorry, I didn't understand"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

i = -1
# Accept user input
if prompt := st.chat_input("What is up?"):
    i += 1
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        assistant_response = random.choice(
            [
                "Tell me about yourself.",
                "What are your strengths?",
                "Can you describe a challenging situation you've faced at work?",
                "Where do you see yourself in five years?",
                "What is your greatest achievement?",
                "How do you handle stress or pressure?",
                "What is your approach to teamwork?",
                "Tell me about a time when you had to overcome a setback.",
            ]
        )
        # Simulate stream of response with milliseconds delay
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
        text_to_speech(assistant_response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
