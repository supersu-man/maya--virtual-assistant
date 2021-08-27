print("Maya is getting Ready...")
import struct
import pyaudio
import pvporcupine
from speech import listen
from linguistics import getIntent
from actions import actions

porcupine = pvporcupine.create(keywords=["computer", "jarvis","hey-maya"])
pa = pyaudio.PyAudio()
audio_stream = pa.open(
                rate=porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=porcupine.frame_length)
print('Welcome..')
while True:
    pcm = audio_stream.read(porcupine.frame_length)
    pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
    keyword_index = porcupine.process(pcm)
    if keyword_index >= 0:
        try:
            text = listen()
            print(text)
            intent, intent_value = getIntent(text)
            print(intent)
            actions(intent, intent_value)
        except: pass
