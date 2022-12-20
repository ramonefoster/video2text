from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import View
from django.views.generic import DetailView
import pytube as youtube
from io import BytesIO
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence
import bcp47
from .models import PostModel, TagsModel
from django.utils.text import slugify

# Create your views here.
class IndexView(View):
    lang_list = bcp47.languages

    def get(self, request):        
        return render(request, 'converter/index.html', {
            "lang": self.lang_list
        })

    def post(self, request):
        url = request.POST['video_url']
        language = request.POST['language']
        #check if already exist
        try:
            x = PostModel.objects.get(url=url) 
        except:
            x = None      
        if x == None:
            erro, txt, video_info = video2audio(url, language)
            keywords = video_info['keywords']
            slug = slugify(video_info['title'])
            if txt: 
                post = PostModel.objects.create(
                    author = video_info['author'],                
                    title = video_info['title'],
                    thumbnail = video_info['thumbnail'],
                    language = str(language),
                    transcript = txt,
                    url = url,
                    slug=slug
                )                
                for key in keywords:
                    tags = TagsModel.objects.create(
                        tag_name=key
                    )
                    post.tags.add(tags)               
                # post.save()
        else:
            slug = x.slug
            
        return HttpResponseRedirect("/converted/"+slug)

class ViewSingle(DetailView):
    template_name = 'converter/single-post.html'
    model = PostModel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.slug_url_kwarg)
        post = PostModel.objects.get(slug=self.kwargs['slug'])
        context["context"] = post 
        return context  

def video2audio(url, language):
    buffer = BytesIO()
    mem_audio = BytesIO() 
    r = sr.Recognizer()
    erro = ''
    text_recognized=''
    video_info = ''
    try:
        yt = youtube.YouTube(url)
        yt.streams.get_by_itag(251).stream_to_buffer(buffer)
        if len(yt.keywords) <= 5:
            keywords = yt.keywords
        else:
            keywords = yt.keywords[0:5]
        video_info = {'author': yt.author,
                        'title': yt.title,
                        'thumbnail': yt.thumbnail_url,
                        'keywords': keywords}
        buffer.seek(0) 
        audio = AudioSegment.from_file(buffer)

        #break audio into smaller pieces for better recognition
        chunks = split_on_silence(audio,
                min_silence_len = 500,
                silence_thresh = audio.dBFS-14,
                keep_silence=500)

        for i, audio_chunk in enumerate(chunks, start=1):            
            audio_chunk.export(mem_audio, format="wav")
            
            with sr.AudioFile(mem_audio) as source:
                audio_listened = r.record(source)                
                try:
                    text = r.recognize_google(audio_listened, language=language)
                except sr.UnknownValueError:
                    erro = "Google Recognition didn't undestand parts of the audio."
                except sr.RequestError:
                    erro = "Request Error."  
                except:
                    erro = "An Error has occurred"
                else:
                    text = f"{text.capitalize()}. "
                    text_recognized += text        
            
    except Exception as e:
        erro = "Invalid Youtube URL or video is corrupted."
    
    return (erro, text_recognized, video_info)

    