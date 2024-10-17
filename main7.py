import os
import speech_recognition as sr
import pyttsx3
import tkinter as tk
from threading import Thread

# Initialize the speech recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Configure text-to-speech speed
engine.setProperty('rate', 180)  # Slightly increase the speech rate for faster responses

# Give the bot a name
bot_name = "Bob: your friendly AI bot"

# Predefined questions and their answers
predefined_questions = {
    "what is your name": f"My name is {bot_name}.",
    "how are you": "I'm feeling as lively as a chatbot can be! Ready to help you.",
    "what do you do": f"I'm {bot_name}, and I can assist with various tasks.",
    "who created you": "I was created by Shreya Sari.",
    "what is the meaning of life": "Life is about learning and experiences.",
    "can you help me with a math problem": "Sure! Tell me the problem.",
    "what is 25 multiplied by 4": "25 multiplied by 4 is 100.",
    "thanks, bob": "You're welcome! Feel free to ask more.",
    "what's your favorite color": "I don’t have feelings, but blue is a popular choice!",
    "can you tell me a joke": "Why did the scarecrow win an award? Because he was outstanding in his field!",
}

def speak(text):
    """Convert text to speech using pyttsx3."""
    engine.say(text)
    engine.runAndWait()

def listen_for_wake_word():
    """Listen for the wake word 'Hey Bob' to activate the system."""
    status_label.config(text="Listening for wake word...")
    while True:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)  # Quick noise adjustment
            audio = recognizer.listen(source, timeout=2)  # Limit listening time to 2 seconds

            try:
                recognized_text = recognizer.recognize_google(audio).lower()

                # Check for the wake word
                if "hey bob" in recognized_text:
                    status_label.config(text="Wake word detected! Ask your question.")
                    return

            except sr.UnknownValueError:
                continue  # Ignore unrecognized audio
            except sr.RequestError:
                status_label.config(text="Speech Recognition service error.")
                continue

def handle_convo():
    """Handle the conversation after wake word detection."""
    status_label.config(text=f"Welcome to {bot_name}!")

    while True:
        listen_for_wake_word()

        wake_word_response = "Hi, how can I assist you today?"
        response_label.config(text=wake_word_response)
        speak(wake_word_response)

        while True:
            status_label.config(text="Listening for your question...")
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)  # Quick noise adjustment
                audio = recognizer.listen(source, timeout=2)  # Limit listening time to 2 seconds

                try:
                    user_input = recognizer.recognize_google(audio).lower()
                    if user_input == "exit":
                        response_label.config(text="Great! Have a wonderful day!")
                        speak("Great! Have a wonderful day!")
                        return

                    # Respond only from the predefined list
                    result = predefined_questions.get(user_input, "Sorry, I don't know how to respond to that.")
                    response_label.config(text=f"{bot_name}: {result}")
                    speak(result)

                    status_label.config(text="Idle")

                except sr.UnknownValueError:
                    response_label.config(text="Sorry, I could not understand the audio.")
                except sr.RequestError:
                    response_label.config(text="Speech Recognition service error.")

def start_conversation():
    """Start the conversation in a new thread."""
    convo_thread = Thread(target=handle_convo, daemon=True)  # Set thread as daemon for quick termination
    convo_thread.start()

def stop_conversation():
    """Stop the ongoing conversation."""
    status_label.config(text="Conversation stopped.")
    root.quit()

# Set up the main Tkinter window
root = tk.Tk()
root.title("Chat with Bob")
root.geometry("400x300")

# Status label
status_label = tk.Label(root, text="Click 'Start Chat' to begin", fg="blue")
status_label.pack(pady=10)

# Response label
response_label = tk.Label(root, text="", fg="green", wraplength=300)
response_label.pack(pady=10)

# Start and Stop buttons
start_button = tk.Button(root, text="Start Chat", command=start_conversation, height=2, width=20)
start_button.pack(pady=10)

stop_button = tk.Button(root, text="Stop Chat", command=stop_conversation, height=2, width=20)
stop_button.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
