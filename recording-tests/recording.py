# https://www.youtube.com/watch?v=av8E8qLZswU

import pyaudio
import wave
import datetime

import speech_recognition as sr


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
now = datetime.datetime.now()
WAVE_OUTPUT_FILENAME = "output-" + str(now.date()) + '-' + str(now.hour) + '-' + str(now.minute) + '-' + str(now.second) + ".wav" 

print(WAVE_OUTPUT_FILENAME)

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* recording")

frames = []

try: 
    while True:
        data = stream.read(CHUNK)
        frames.append(data)
except KeyboardInterrupt:
    pass

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()


r = sr.Recognizer()

# open the file
with sr.AudioFile(WAVE_OUTPUT_FILENAME) as source:
    # listen for the data (load audio to memory)
    audio_data = r.record(source)
    # recognize (convert from speech to text)
    text = r.recognize_google(audio_data)
    print(text)