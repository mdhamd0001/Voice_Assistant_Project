import speech_recognition as sr
import webbrowser
import pyttsx3
import google.generativeai as genai
import os
import playlist

# Initialize the recognizer and pyttsx3 engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.setProperty('rate', 130)
    engine.say(text)
    engine.runAndWait()

def AI(t):
    # Ensure the API key is set as an environment variable
    os.environ["API_KEY"] = "AIzaSyCAPnaXsnmKh8ZQeTzwjYwVZ2IK183o4oM"  # Replace with your actual API key

    try:
        # Configure the API key
        genai.configure(api_key=os.environ["API_KEY"])

        # Create a model instance (assuming this is the correct way to initialize the model)
        model = genai.GenerativeModel('gemini-1.5-flash')

        # Generate content
        response = model.generate_content(t + " Answer this atmost 4 lines")

        # Print the response and use text-to-speech to speak it
        print(response.text)
        speak(response.text)

    except KeyError:
        print("API key not found. Please set the API key in the environment variables.")
    except AttributeError as e:
        print(f"Attribute error: {e}. Check the method and attribute names.")
    except Exception as e:
        print(f"An error occurred: {e}")

def command(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ", 1)[1]
        # Assuming you have a playlist module with a dictionary named 'music'
        link = playlist.music.get(song, "")
        if link:
            webbrowser.open(link)
        else:
            speak(f"Sorry, I couldn't find the song {song} in the playlist.")
    else:
        AI(c.lower())

def voicerecognizer():
    speak("Salam Walekum bhaijaan")
    while True:
        with sr.Microphone() as source:
            print("Adjusting for ambient noise, please wait...")
            recognizer.adjust_for_ambient_noise(source, duration=0.2)
            print("Listening for your speech...")
            audio = recognizer.listen(source)

            try:
                print("Recognizing speech...")
                text = recognizer.recognize_google(audio)
                print(f"You said: {text}")
                if text.lower() == "hey jarvis":
                    speak("Yes sir")
                    with sr.Microphone() as source:
                        recognizer.adjust_for_ambient_noise(source, duration=0.2)
                        print("Listening for your command...")
                        audio = recognizer.listen(source)
                        print("Recognizing command...")

                        text = recognizer.recognize_google(audio)
                        command(text)

            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand the audio")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")

if __name__ == "__main__":
    try:
        voicerecognizer()
    except Exception as e:
        speak("An error occurred, please try again.")
        print(f"An error occurred: {e}")
