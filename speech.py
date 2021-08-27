import speech_recognition as sr
from gtts import gTTS
from io import BytesIO

from pydub import AudioSegment
from pydub.playback import play

r = sr.Recognizer()

def playSound(file):
    song = AudioSegment.from_file(file, format="mp3")
    play(song)

def say(text):
    tts = gTTS(text=text, lang='en', tld='ca')
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    playSound(fp)

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        playSound('utils/listenStart.wav')
        audio = r.listen(source)
        audioText = r.recognize_google(audio)
        return audioText