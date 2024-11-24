import speech_recognition as sr
from TTS_STT.TTS import speak
import eel

@eel.expose
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        # eel.DisplayMessage("Listening...")
        r.pause_threshold = 2  # Reduced pause threshold for quicker response
        audio = r.listen(source, timeout=1000000000000000000000000, phrase_time_limit=5)  # Reduced timeout and phrase time limit
    
    try:
        print("Recognizing....")
        eel.DisplayMessage("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        # print(f"user said: {query}")
        # eel.DisplayMessage(query)
        
    except Exception as e:
        speak("Could you please repeat again...")
        return "none"
    return query