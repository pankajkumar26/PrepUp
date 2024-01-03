import pyttsx3
import speech_recognition as sr
from gtts import gTTS
import random

from bardapi import Bard

import time
import os
import random

os.environ["_BARD_API_KEY"] = "eQgrkRP0VhxBpFFudNP2weFG3GB8VJsCayLSBiXTvNXWsr6-peAkk6ebpjUAd3LknrFnyg."


def get_completion(prompt):
    response = Bard().get_answer(prompt)["content"]
    return response

def display_and_store_response(question, answer, review):
    # print(review)
    if not os.path.exists("Report"):
        with open("Report.txt", "a") as file:
            file.writelines(f"\n\nQuestion: {question} \n\nAnswer: {answer} \n\nReview: {review}\n" )
    else:
        random_number = random.randrange(1000,9000)
        filename = f"Report_{random_number}.txt"
        with open(filename, "a") as file:
            file.writelines(f"\n\nQuestion: {question} \n\nAnswer: {answer} \n\nReview: {review}\n" )


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
    # return random.choice(questions)
    return questions[index]


def request_bard(input_text, question):
    try:
        prompt = f"""
                Your task is to act as a Text Analyzer.
                I'll give you text which is basically the answers given by a person for the questions asked. 
                And your job is to analyse the answer for that question and tell how accurate his answer was and how many grammar mistakes he had.
                Don't be conversational. I need a plain 10-40 word answer for this.
                Question and the Answer is shared below, delimited with triple backticks:
                ```{question}```,
                ```{input_text}```
                
                """
        return get_completion(prompt)

    except :
        return "Error: Unable to connect to the server. Please try again later."


# request_bard(
#     "My strengths includes learning new technology quickly and solving the problems based on it",
#     "What are your strengths?",
# )


def interview_chatbot():
    text_to_speech("Hello! I am your interview assistant. How can I help you today?")
    user_responses = []
    length = 4
    i = 0
    while i < length:
        question = get_question(i)
        text_to_speech(question)

        user_input = speech_to_text()
        user_responses.append(user_input)

        if "exit" in user_input.lower():
            text_to_speech("Goodbye! Have a great day.")
            break

        text_to_speech("Please wait while I process your response.")
        bard_response = request_bard(user_input, question)

        # Display BARD's response to the user and store it for later use
        display_and_store_response(question, user_input, bard_response)
        text_to_speech(bard_response)
        i += 1


if __name__ == "__main__":
    interview_chatbot()
