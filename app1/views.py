import requests
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

# Register view
def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        name=request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            try:
                User.objects.create_user(username=username,first_name=name, email=email, password=password)
                messages.success(request, 'Registration successful! Please log in.')
                return redirect('login')
            except:
                messages.error(request, 'Username already exists.')
        else:
            messages.error(request, 'Passwords do not match.')

    return render(request, 'register.html')

# Login view
def login_view(request):
    if request.user.is_authenticated:  # If the user is already logged in
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login') 

@login_required
def home(request):
    name=request.user.first_name
    return render(request,'home.html',{'name':name})


def track_download(request):

    song=request.GET['song']
    track_name = song
    quality = 'hq'  

    # Make the API request to get the track data
    url = f'https://spotify-scraper.p.rapidapi.com/v1/track/download/soundcloud?track={track_name}&quality={quality}'
    headers = {
        "x-rapidapi-key": "057f69f4a6mshc4b580a0702816bp1895a1jsnc76ab04306a0",
        "x-rapidapi-host": "spotify-scraper.p.rapidapi.com"
    }


    response = requests.get(url, headers=headers)
    data = response.json()
    if response.status_code == 200:
        
        # Get SoundCloud and Spotify track details
        soundcloud_track = data.get('soundcloudTrack', {})
        spotify_track = data.get('spotifyTrack', {})
        
        # Prepare context to pass to the template
        context = {
            'soundcloud_track': soundcloud_track,
            'spotify_track': spotify_track,
        }

        return render(request, 'search.html', context)
    else:
        return render(request,'Error.html')