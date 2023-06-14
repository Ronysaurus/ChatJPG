import vlc
import sounddevice as sd
import speech_recognition as sr
import numpy as np
from scipy.io import wavfile
from revChatGPT.V1 import Chatbot
from gtts import gTTS

fs = 44100
seconds = 5

language = 'es'
domain = 'com.mx'

r = sr.Recognizer()

chatbot = Chatbot(config={
  "access_token": "<access_token>",
  "disable_history": "true"
})

while(True):
    input("presiona enter para iniciar la grabacion")
    try:
        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
        sd.wait()
        y = (np.iinfo(np.int32).max * (myrecording/np.abs(myrecording).max())).astype(np.int32)
        wavfile.write('stt.wav', fs, y)
        with sr.AudioFile('stt.wav') as source:
            audio_data = r.record(source)
            prompt = r.recognize_google(audio_data, language='es-MX')
            print(prompt)
            response = ""
            for data in chatbot.ask(prompt):
                response = data["message"]
            print(f'chat: {response}')
            tts = gTTS(text=response, lang=language, tld=domain, slow=False)
            tts.save("tts.mp3")
            p = vlc.MediaPlayer("tts.mp3")
            p.play()
    except Exception as e:
        print(e)