from vosk import Model, KaldiRecognizer
import os
import json

if not os.path.exists("model"):
    print ("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
    exit (1)

import pyaudio

dict = {"привет": "echo Да, мой господ+ин | festival --tts --language russian",
	"подскажи время" : "echo Сейчас десять вечера | festival --tts --language russian"}

model = Model("model")
rec = KaldiRecognizer(model, 16000)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

while True:
	data = stream.read(4000)
	if len(data) == 0:
		break
	if rec.AcceptWaveform(data):
		text = json.loads(rec.Result())['text']
		print(text)
		tmp = dict.get(text)
		try:
			if tmp:
				os.system(tmp)
		except BaseException:
			print("хуй тебе")
			
	    

        #os.system(dict[tmp])
        
	else:
		#print(rec.PartialResult().split('"partial" : "'))
		print(rec.PartialResult())

print(rec.FinalResult())
