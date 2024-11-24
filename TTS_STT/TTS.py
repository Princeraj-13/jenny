import os
import logging
from dotenv import load_dotenv
import playsound
import eel
import time
import uuid

load_dotenv()

from deepgram import (
    DeepgramClient,
    SpeakOptions,
)

# Set your API key here
API_KEY = os.getenv("DG_API_KEY")
filename = f"Audio/output_{uuid.uuid4()}.mp3"

def speak(text):
    try:
        print(f"Jenny: {text}")
        SPEAK_TEXT = {"text": text}
        deepgram = DeepgramClient(API_KEY)
        options = SpeakOptions(
            model="aura-asteria-en",
        )
        response = deepgram.speak.rest.v("1").save(filename, SPEAK_TEXT, options)
        # time.sleep(1)
        playsound.playsound(filename)
        if os.path.exists(filename):
            os.remove(filename)
        return filename
    except Exception as e:
        print(f"Exception: {e}")