from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import View
import pytube as yt
from io import BytesIO
import sys
from scipy.io.wavfile import write
import speech_recognition as sr
import numpy as np
import ffmpeg

# Create your views here.
class IndexView(View):
    def get(self, request):
        return render(request, 'converter/index.html')

    def post(self, request):
        url = request.POST['video_url']
        video2audio(url)
        return HttpResponseRedirect('/converter')

def video2audio(url):
    buffer = BytesIO()
    mem_audio = BytesIO() 
    r = sr.Recognizer()
    try:
        youtube = yt.YouTube(url)
        youtube.streams.get_audio_only().stream_to_buffer(buffer)

        buffer.seek(0) 
        dat = np.asarray(bytearray(buffer.read()), dtype=np.int32)
        write(mem_audio, 16000, dat)
        with sr.AudioFile(mem_audio) as source:
            try:
                print("Starting to get text")               
                audio = r.record(source)                
                print(source.DURATION)
                txt = r.recognize_google(audio, language="en-US", show_all=True)
                print(txt)
            except Exception as e:
                print("ERRO", e)        
    except Exception as e:
        print("err", e)
    
    return