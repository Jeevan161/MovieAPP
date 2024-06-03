import requests
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
import requests as http_requests
from django.http import JsonResponse
from django.shortcuts import render

from movies.models import Playlist


def get_movie_details(imdb_id):
    api_key = 'your_omdb_api_key'  # Replace with your OMDB API key
    url = f"http://www.omdbapi.com/?i={imdb_id}&apikey=97d611c7"
    response = requests.get(url)
    return response.json()


def home(request):
    playlist_id = 25
    try:
        playlist = Playlist.objects.get(id=playlist_id)
        movies = playlist.movies.all()
    except Playlist.DoesNotExist:
        playlist = None
        movies = []

    user_name = request.user.first_name if request.user.is_authenticated else None

    context = {
        'playlist': playlist,
        'movies': movies,
        'user_name': user_name,
    }
    return render(request, 'temps/home.html', context)


def search(request):
    if request.method == 'POST':
        query = request.POST.get('query', '')
        page = request.POST.get('page', '1')
        if len(query) >= 3:
            # Use the provided API URL with pagination
            api_url = f"http://www.omdbapi.com/?apikey=97d611c7&s={query}&page={page}"
            response = http_requests.get(api_url)
            data = response.json()
            print(data)
            return JsonResponse(data)  # Return the API response as JSON

    return render(request, 'temps/Search.html')

