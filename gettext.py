import speech_recognition as sr
r = sr.Recognizer()
audio = r.record(sr.AudioFile("hello_world.wav"))

try:
    s = r.recognize_google(audio)
    print("Text: "+s)
except Exception as e:
    print("Exception: "+str(e))