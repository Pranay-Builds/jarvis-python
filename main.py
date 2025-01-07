import pyttsx3
import speech_recognition as sr
import webbrowser
import musicLibrary
import requests
from datetime import datetime
import google.generativeai as genai
import pyjokes

# In this script, you can replace "yourgeminiapikey" with your actual Google Gemini API key 
# to get AI-generated responses using the Gemini model.

# Initialize recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "yournewsapikey"

# Function to make Jarvis speak
def speak(message):
    engine.say(message)
    engine.runAndWait()

# Function to process commands
def processCommand(c):
    
    if "open google" in c.lower():
        webbrowser.open("https://www.google.com")
    elif "open github" in c.lower():
        webbrowser.open("https://github.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://www.youtube.com")
    elif "open spotify" in c.lower():
        webbrowser.open("https://open.spotify.com")
    elif "open chat" in c.lower():
        webbrowser.open("https://chat.openai.com")
    elif "open roblox" in c.lower():
        webbrowser.open("https://roblox.com")
    elif "weather" in c.lower():
        city = c.lower().split(" ")[1]
        webbrowser.open(f'https://google.com/search?q=weather+{city}')
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)
    elif "wordle" in c.lower():
        webbrowser.open("https://www.nytimes.com/games/wordle/index.html")  
    elif "news" in c:
        keyword = c.lower().split(" ")[1]
        url = f"https://newsapi.org/v2/everything?q={keyword}&apiKey={newsapi}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                articles = data.get('articles', [])
                
                if articles:
                    speak("Here are the latest news articles:")
                    
                    # Speak the headlines and descriptions of the articles
                    for article in articles:
                        title = article.get('title', 'No title available')
                        description = article.get('description', 'No description available')
                        
                        speak(f"Title: {title}")
                        speak(f"Description: {description}")
                        speak("------")
                else:
                    speak("Sorry, I couldn't find any news articles for that topic.")
            else:
                speak("Failed to fetch news. Please check your network or API key.")
        except Exception as e:
            speak(f"An error occurred: {str(e)}")
    elif "joke" in c:
        joke = pyjokes.get_joke()
        if joke:
            speak(joke)
        else:
            speak("Sorry, I couldn't find a joke for you. Please try again.")
    elif "time" in c:
        currentime = datetime.now().strftime("%H:%M")
        speak(f"The current time is {currentime}")
    elif "search" in c:
        query = c.lower().split("search")[1].strip()
        if query:
            webbrowser.open(f'https://www.google.com/search?q={query}')
        else:
            speak("Please provide a search query.")
    else:
        try:
            genai.configure(api_key="yourgeminiapikey")
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(f"You are a desktop assistant, and {c} is your command. Please respond as a desktop assistant and dont use text decorations (astericks, underscores, etc)")
            if response:
                speak(response.text)
            else:
                speak("I could not understand that, Please try again")
        except Exception as e:
            speak(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    speak("Initializing Jarvis...")

    while True:
        try:
            # Listening for the trigger word "Jarvis"
            with sr.Microphone() as source:
                print("Say something!")
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=1)

            word = recognizer.recognize_google(audio).lower()
            print(f"You said: {word}")

            # If "jarvis" is said, activate Jarvis and wait for further commands
            if word == "jarvis":
                speak("Sup, how can I assist you?")
                
                # Listen for the follow-up command
                with sr.Microphone() as source:
                    print("Jarvis Active")
                    audio = recognizer.listen(source)

                command = recognizer.recognize_google(audio).lower()
                processCommand(command)

        except sr.UnknownValueError:
            print("Sorry, I didn't catch that.")
        except sr.RequestError:
            print("Network error. Please check your connection.")
        except Exception as e:
            print(f"Error: {e}")
