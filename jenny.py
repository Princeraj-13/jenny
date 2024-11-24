import pyttsx3
import speech_recognition as sr
import os
import cv2
import random
from requests import get
from datetime import datetime, timedelta
import pywhatkit as kit  
import logging
import pyautogui
import playsound
import time
import eel
from dotenv import load_dotenv
import pyaudio
import psutil

# file import below
from AI_ChatBot.write_ai import write
from AI_ChatBot.score import score
from AI_ChatBot.groq_chat import generate
from TTS_STT.TTS import speak
from TTS_STT.takecommand import takecommand
from AI_ChatBot.pdf import generate_pdf

# Load environment variables
load_dotenv()

# Initialize Eel
eel.init("www")
os.system('start msedge.exe --app="http://localhost:5500/www/index.html"')

# Global variable for sleep mode
sleep_mode = False


# Expose the functions to Eel
@eel.expose
def jenny_speak(text):
    speak(text)

@eel.expose
def jenny_takecommand():
    return takecommand()

@eel.expose
def get_system_info():
    cpu_usage = psutil.cpu_percent(interval=1)  # Get CPU usage percentage
    ram_usage = psutil.virtual_memory().percent  # Get RAM usage percentage
    process_count = len(psutil.pids())  # Get the number of processes

    return {
        "cpu": cpu_usage,
        "ram": ram_usage,
        "processes": process_count
    }

@eel.expose
def jenny_generate(query):
    result = generate(query)
    if result is not None:
        _, response = result
        return response
    return "I didn't understand that."


@eel.expose
def jenny_generate_pdf(query):
    speak("on which topic you want to generate pdf sir?")
    query = takecommand()
    result = generate_pdf(query)
    if result is not None:
        _, response = result
        return response
    return "I didn't understand that."


@eel.expose
def jenny_write(query):
    result = write(query)
    if result is not None:
        _, response = result
        return response
    return "I didn't understand that."

@eel.expose
def jenny_score(query):
    result = score(query)
    if result is not None:
        _, response = result
        return response
    return "I didn't understand that."


# change password
# for i in range(3):
#     code = input("Please Enter Password :- ")
#     pw_file = open("password.txt","r")
#     pw = pw_file.read()
#     pw_file.close()
#     if (code==pw):
#         break
#     elif (i==2 and code!=pw):
#         exit()

#     elif (code!=pw):
        # speak("password you entered is wrong. sir, please try again")

@eel.expose
def change_password(new_pw):
    with open("password.txt", "w") as new_password_file:
        new_password_file.write(new_pw)
    return f"Your new password is {new_pw}"


def wish():
    hour = int(datetime.now().hour)
    tt = time.strftime("%I:%M %p")
    
    if hour >= 0 and hour <= 12:
        jenny_speak(f"Goodmorning sir, it's {tt}, how may I assist you today?")
        
    elif hour >= 12 and hour <= 18:
        jenny_speak(f"Good afternoon sir, it's {tt}, how may I assist you today?")
    else:
        jenny_speak(f"Hello sir, it's {tt}, how may I assist you today?")

if __name__ == "__main__":
    wish()
    while True:
        query = jenny_takecommand().lower()

        if "jenny open" in query or "jennie open" in query or "jeny open" in query:
            query = query.replace("jenny", "").replace("open", "").replace("the", "")
            jenny_speak("Opening " + query + " sir")
            pyautogui.press("super")
            pyautogui.typewrite(query)
            pyautogui.press("enter")

        elif "change password" in query:
            new_pw = input("Enter the new password\n")
            response = change_password(new_pw)
            jenny_speak(response)

        elif 'keep' in query or "sleep" in query:
            jenny_speak("Okay sir, call me anytime you need")
            sleep_mode = True

        elif "write" in query:
            result = jenny_write(query)
            jenny_speak(result)

        elif "test" in query or "exam" in query:
            result = jenny_score(query)
            jenny_speak(result)

        elif "pdf" in query or "PDF" in query or "generate pdf" in query or "generate PDF" in query:
            result = jenny_generate_pdf(query)
            print(result)

        # elif "close" in query or "terminate" in query:
        #     terminate_program()


        else:
            response = jenny_generate(query)
            jenny_speak(response)

        while sleep_mode:
            query = jenny_takecommand()
            if 'wake' in query or "awake" in query:
                jenny_speak("I am back sir, how can I assist you?")
                sleep_mode = False

eel.start('www/index.html', mode=None, host='localhost', block=True)