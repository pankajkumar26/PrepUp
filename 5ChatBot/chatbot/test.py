import streamlit as st
import pyttsx3
import speech_recognition as sr
# from gtts import gTTS
import random
from bardapi import Bard
import os

os.environ["_BARD_API_KEY"] = "eQgrkaLkZrpY7I5LkFfbyWxPPtGazvKK3mJ8A4RG62mVqO7TjWXyJ2SKN2jxtbVoXV2Txg."


def get_completion(prompt):
    response = Bard().get_answer(prompt)["content"]
    return response


def display_and_store_response(question, answer, review):
    if not os.path.exists("Report"):
        with open("Report.txt", "a") as file:
            file.writelines(f"\n\nQuestion: {question} \n\nAnswer: {answer} \n\nReview: {review}\n")
    else:
        random_number = random.randrange(1000, 9000)
        filename = f"Report_{random_number}.txt"
        with open(filename, "a") as file:
            file.writelines(f"\n\nQuestion: {question} \n\nAnswer: {answer} \n\nReview: {review}\n")


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
        st.write("Please start speaking...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            st.write("Recognizing ...")
            text = recognizer.recognize_google(audio, language="en-in")
            return text
        except Exception as e:
            st.write("Sorry, I didn't understand")
            return "Sorry, I didn't understand"


def get_question(index):
    questions = [
        "Tell me about yourself.",
        "What are your strengths?",
        "Can you describe a challenging situation you've faced at work?",
        "Where do you see yourself in five years?",
        "What is your greatest achievement?",
        "How do you handle stress or pressure?",
        "What is your approach to teamwork?",
        "Tell me about a time when you had to overcome a setback.",
    ]
    return questions[index]


def request_bard(input_text, question):
    try:
        prompt = f"""
                Your task is to act as a Text Analyzer.
                I'll give you text which is basically the answers given by a person for the questions asked. 
                And your job is to analyze the answer for that question and tell how accurate his answer was and how many grammar mistakes he had.
                Don't be conversational. I need a plain 10-40 word answer for this.
                Question and the Answer are shared below, delimited with triple backticks:
                ```{question}```,
                ```{input_text}```
                
                """
        return get_completion(prompt)
    except:
        return "Error: Unable to connect to the server. Please try again later."


def interview_chatbot():
    text_to_speech("Hello! I am your interview assistant. How can I help you today?")
    user_responses = []
    bard_responses = []
    length = 4
    i = 0
    while i < length:
        question = get_question(i)
        text_to_speech(question)

        st.write("Your Response:")
        user_input = st.text_input("Speak or type your response:")
        user_responses.append(user_input)

        if "exit" in user_input.lower():
            text_to_speech("Goodbye! Have a great day.")
            break

        st.write("BARD's Response:")
        st.write("Please wait while I process your response.")
        bard_response = request_bard(user_input, question)
        bard_responses.append(bard_response)

        # Display BARD's response to the user and store it for later use
        display_and_store_response(question, user_input, bard_response)
        text_to_speech(bard_response)
        i += 1

    # Display chat-like format of questions, user responses, and BARD's responses
    st.write("Chat History:")
    for q, user_resp, bard_resp in zip(questions[:i], user_responses, bard_responses):
        st.write(f"Question: {q}")
        st.write(f"Your Response: {user_resp}")
        st.write(f"BARD's Response: {bard_resp}")
        st.write("\n")


if __name__ == "__main__":
    interview_chatbot()
