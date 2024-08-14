import os
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Ticker
from django.shortcuts import render
from .forms import TickerTextForm, UserForm
from .create_ticker import create_ticker
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q

# Create your views here.
def loginPage(request):
    page = 'login'
    
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist")
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exists')        
    context = {'page': page}
    return render(request, 'tickerapp/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = UserCreationForm()
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')
    return render(request, 'tickerapp/login_register.html', {'form':form})


def home(request):
    if request.method == 'POST':
        form = TickerTextForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            filename = form.cleaned_data['filename']
            video_path = create_ticker(text, filename)
            #print(video_path)
            
            # Сохранение данных в базе данных
            owner = request.user if request.user.is_authenticated else None
            video_request = Ticker(owner=owner, text=text, filename=filename)
            video_request.video_file.save(os.path.basename(video_path), open(video_path, 'rb'))
            video_request.save()
            
            # Удаление временного файла
            os.remove(video_path)
            
            if 'create_and_download' in request.POST:
                return redirect('download', pk=video_request.id)
            
            return redirect('home')
    else:
        form = TickerTextForm()
    
    tickers = None
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        tickers = user.ticker_set.all().order_by('-timestamp').values()[:5]
    context = {'form': form, 'tickers': tickers}
    return render(request, 'tickerapp/home.html', context=context)


def downloadPage(request, pk):
    ticker = Ticker.objects.get(id=pk)
    if (request.user.is_authenticated & (request.user == ticker.owner)) | (ticker.owner == None):
        video_path = str(ticker.video_file)
        with open(video_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='video/x-msvideo')
            response['Content-Disposition'] = f'attachment; filename="{ticker.filename}.avi"'
        return response
    else:
        return HttpResponse('You are not allowed here!')
 
    
@login_required(login_url='login')
def userProfile(request, pk):
    user = User.objects.get(id=pk)
    tickers = user.ticker_set.all().order_by('-timestamp').values()
    context = {'user': user, 'tickers': tickers}
    return render(request, 'tickerapp/profile.html', context)

@login_required(login_url='login')
def userEdit(request, pk):
    user = User.objects.get(id=pk)
    form = UserForm(instance=user)
    
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=user.id)
    
    context = {'user': user, 'form': form}
    return render(request, 'tickerapp/edit_profile.html', context)