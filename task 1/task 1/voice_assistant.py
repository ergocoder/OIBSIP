import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import wikipedia

engine = pyttsx3.init()
engine.setProperty('rate', 160)

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio, language="en-in").lower()
        print(f"You said: {command}")
        return command
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError:
        speak("Network error.")
        return ""

def tell_time():
    time_str = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The time is {time_str}")

def tell_date():
    date_str = datetime.datetime.now().strftime("%B %d, %Y")
    speak(f"Today's date is {date_str}")

def search_web(query):
    if query:
        speak(f"Searching Google for {query}")
        webbrowser.open(f"https://www.google.com/search?q={query}")
    else:
        speak("Please say what you want me to search for.")

def open_website(site_name):
    sites = {
        "google": "https://www.google.com",
        "youtube": "https://www.youtube.com",
        "github": "https://www.github.com"
    }
    if site_name in sites:
        speak(f"Opening {site_name}")
        webbrowser.open(sites[site_name])
    else:
        speak(f"I don't know {site_name}, searching instead.")
        search_web(site_name)

def wikipedia_search(query):
    try:
        summary = wikipedia.summary(query, sentences=2)
        speak(summary)
    except wikipedia.exceptions.DisambiguationError:
        speak("That term is ambiguous, please be more specific.")
    except wikipedia.exceptions.PageError:
        speak("I couldn't find anything on Wikipedia.")

def main():
    speak("This is your voice assistant. How can I help you?")
    while True:
        command = listen()

        if "hello" in command:
            speak("Hello! How are you today?")
        elif "time" in command:
            tell_time()
        elif "date" in command:
            tell_date()
        elif command.startswith("search for"):
            query = command.replace("search for", "").strip()
            search_web(query)
        elif command.startswith("search"):
            query = command.replace("search", "").strip()
            search_web(query)
        elif command.startswith("open"):
            site = command.replace("open", "").strip()
            open_website(site)
        elif "wikipedia" in command:
            query = command.replace("wikipedia", "").strip()
            wikipedia_search(query)
        elif "exit" in command or "quit" in command:
            speak("Goodbye!")
            break
        elif command:
            speak("Sorry, I don't know that command yet.")

if __name__ == "__main__":
    main()
