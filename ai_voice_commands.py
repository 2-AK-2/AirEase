import os
import speech_recognition as sr
from dotenv import load_dotenv
from transformers import pipeline

# Load environment variables from .env file
load_dotenv()

# Set up Hugging Face pipeline for intent recognition (using a zero-shot classification model)
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        # Convert speech to text
        user_input = recognizer.recognize_google(audio).lower()
        print(f"You said: {user_input}")
        
        # Send user input to Hugging Face for intent recognition
        process_command(user_input)

    except sr.UnknownValueError:
        print("Could not understand audio. Try again.")
    except sr.RequestError:
        print("Error with the recognition service.")

def process_command(user_input):
    # Define candidate labels for the classification model
    candidate_labels = ["turn on cooling", "increase airflow", "decrease airflow", "turn off cooling", "stop cooling"]

    # Use Hugging Face model to classify the command
    result = classifier(user_input, candidate_labels)

    # Extract the most likely intent
    intent = result['labels'][0]
    print(f"AI Decision: {intent}")

    # Simulated hardware actions based on recognized intent
    if "turn on cooling" in intent or "activate cooling" in intent:
        print("Turning on cooling...")
    elif "increase airflow" in intent or "boost cooling" in intent:
        print("Increasing airflow...")
    elif "turn off cooling" in intent or "stop cooling" in intent:
        print("Turning off cooling...")
    else:
        print("Command not recognized. Try again.")

# Run the voice control function
recognize_speech()
