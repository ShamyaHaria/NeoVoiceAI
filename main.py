import speech_recognition as sr
import os
import webbrowser
import openai
from config import apikey
import datetime
import random
import numpy as np

chat_log = ""

def chat(query):
    global chat_log
    print(chat_log)
    openai.api_key = apikey
    chat_log += f"Shamya: {query}\n Xander: "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=chat_log,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    speak(response["choices"][0]["text"])
    chat_log += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]

def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    text += response["choices"][0]["text"]
    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip() }.txt", "w") as f:
        f.write(text)

def speak(text):
    os.system(f'say "{text}"')

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Some Error Occurred. Sorry from Xander"

if __name__ == '__main__':
    speak('Hello! I am Xander A I')
    while True:
        print("Listening...")
        query = takeCommand()

        sites = [["youtube", "https://www.youtube.com/"], ["google", "https://www.google.com/"], ["gmail", "https://mail.google.com"],["mysite", "https://shamyaharia.github.io/"]]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                speak(f"Opening {site[0]}")
                webbrowser.open(site[1])

            if "play music" in query:
                musicPath = "/Users/shamya/Downloads/Cigarettes-JuiceWRLD.mp3"
                os.system(f"play {musicPath}")

            elif "the time" in query:
                strfTime = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"The time is {strfTime}")

            elif "open facetime".lower() in query.lower():
                os.system(f"open /System/Applications/FaceTime.app")

            elif "open photos".lower() in query.lower():
                os.system(f"open /System/Applications/Photos.app")

            elif "Using artificial intelligence".lower() in query.lower():
                ai(prompt=query)

            elif "Xander Quit".lower() in query.lower():
                exit()

            elif "reset chat".lower() in query.lower():
                chat_log = ""

            else:
                chat(query)
