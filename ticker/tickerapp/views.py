import os
from django.http import HttpResponse
from .models import VideoRequest
from django.shortcuts import render
from .forms import TickerTextForm
from .create_ticker import create_ticker

# Create your views here.

def home(request):
    if request.method == 'POST':
        form = TickerTextForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            video_path = create_ticker(text)
            
            # Сохранение данных в базе данных
            video_request = VideoRequest(text=text)
            video_request.video_file.save(os.path.basename(video_path), open(video_path, 'rb'))
            video_request.save()
            
            # Возврат видеофайла в HTTP-ответе
            with open(video_path, 'rb') as f:
                response = HttpResponse(f.read(), content_type='video/x-msvideo')
                response['Content-Disposition'] = 'attachment; filename="output.avi"'
            
            # Удаление временного файла
            os.remove(video_path)
            
            return response
    else:
        form = TickerTextForm()
    
    return render(request, 'tickerapp/home.html', {'form': form})


def video_view(request):
    text = request.GET.get('text', 'Running Text Sample')

    video_path = create_ticker(text)

    # Сохранение данных в базе данных
    video_request = VideoRequest(text=text)
    video_request.video_file.save(os.path.basename(video_path), open(video_path, 'rb'))
    video_request.save()

    # Открытие видеофайла и возврат в HTTP-ответе
    with open(video_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='video/x-msvideo')
        response['Content-Disposition'] = f'attachment; filename="{video_path}.avi"'

    # Удаляем временный файл
    os.remove(video_path)
    return response