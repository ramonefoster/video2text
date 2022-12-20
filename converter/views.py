from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import View
import pytube as youtube
from io import BytesIO
import sys
from scipy.io.wavfile import write
import speech_recognition as sr
import numpy as np
import datetime
from pydub import AudioSegment

# Create your views here.
class IndexView(View):
    def get(self, request):
        return render(request, 'converter/index.html')

    def post(self, request):
        url = request.POST['video_url']
        erro, txt = video2audio(url)
        return render(request, 'converter/index.html', {'error': erro, 'text_result': txt})

def video2audio(url):
    buffer = BytesIO()
    mem_audio = BytesIO() 
    r = sr.Recognizer()
    erro = ''
    # teste url = https://youtu.be/naIkpQ_cIt0
    try:
        yt = youtube.YouTube(url)
        yt.streams.get_by_itag(251).stream_to_buffer(buffer)
        print(yt.streams.get_audio_only().audio_codec)

        buffer.seek(0) 
        audio = AudioSegment.from_file(buffer)
        audio.export(mem_audio, format="wav")

        with sr.AudioFile(mem_audio) as source:
            try:
                print("Starting to get text")               
                audio = r.record(source)                
                print("Duração do audio: ", datetime.timedelta(seconds=source.DURATION))
                txt = r.recognize_google(audio, language="en-US", show_all=True)
                print(txt)
            except sr.UnknownValueError:
                erro = "Google Recognition didn't undestand the audio."  
            except:
                erro = "An Error has occurred"
    except Exception as e:
        erro = "Invalid Youtube URL or video is corrupted."
    
    return (erro, txt)