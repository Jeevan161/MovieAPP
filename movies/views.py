import json

import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect

from movies.models import Playlist, Movie


# Create your views here.
@login_required
def create_playlist(request):
    storage = messages.get_messages(request)
    for _ in storage:
        pass  # Iterate over messages to clear them
    if request.method == 'POST':
        name = request.POST.get('name')
        imdb_id = request.POST.get('imdb_id')

        # Fetch additional movie details from OMDB API
        movie_details = fetch_movie_details(imdb_id)

        # Create the playlist
        playlist = Playlist.objects.create(name=name, user=request.user)

        # Create or update the movie object
        movie, created = Movie.objects.update_or_create(
            imdb_id=imdb_id,
            defaults={
                'mv_name': movie_details.get('Title', ''),
                'mv_year': movie_details.get('Year', ''),
                'mv_poster': movie_details.get('Poster', '')
            }
        )

        # Add movie to playlist
        playlist.movies.add(movie)
        messages.success(request,"Playlist created and movie added successfully")
        return render(request,"temps/Search.html")
def delete_mv(request, playlist_id, imdb_id):
    storage = messages.get_messages(request)
    for _ in storage:
        pass  # Iterate over messages to clear them
    if request.method == 'POST':
        try:
            playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
            movie = get_object_or_404(Movie, imdb_id=imdb_id)

            # Remove the movie from the playlist
            playlist.movies.remove(movie)
            messages.error(request, 'Movie removed from playlist')
            return redirect('/playlists')
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:

        return HttpResponseBadRequest("Invalid request method")


def add_to_playlist_c(request, imdb_id,playlist_id):
    storage = messages.get_messages(request)
    for _ in storage:
        pass  # Iterate over messages to clear them
    try:
        playlist = Playlist.objects.get(id=playlist_id, user=request.user)
        movie, created = Movie.objects.get_or_create(imdb_id=imdb_id)
        playlist.movies.add(movie)
        messages.success(request,"Movie added to playlist successfully!")
        return render(request,'temps/Search.html',{'message': 'Movie added to playlist successfully!'})
    except Playlist.DoesNotExist:
        return JsonResponse({'error': 'Playlist not found!'}, status=404)
    except Movie.DoesNotExist:
        return JsonResponse({'error': 'Movie not found!'}, status=404)

@login_required()
def get_playlists(request):
    if request.user.is_authenticated:
        playlists = Playlist.objects.filter(user__email=request.user.email)
        playlist_data = [{'id': playlist.id, 'name': playlist.name, 'num_movies': playlist.movies.count()} for playlist in playlists]
        return JsonResponse({'playlists': playlist_data})
    else:
        return JsonResponse({'error': 'User is not authenticated'}, status=401)

@login_required
def add_to_playlist(request):
    storage = messages.get_messages(request)
    for _ in storage:
        pass  # Iterate over messages to clear them
    if request.method == 'POST':
        data = json.loads(request.body)
        imdb_id = data['imdb_id']
        playlist_id = data['playlist_id']

        # Fetch additional movie details from OMDB API
        movie_details = fetch_movie_details(imdb_id)

        # Create or update the movie object
        movie, created = Movie.objects.update_or_create(
            imdb_id=imdb_id,
            defaults={
                'mv_name': movie_details.get('Title', ''),
                'mv_year': movie_details.get('Year', ''),
                'mv_poster': movie_details.get('Poster', '')
            }
        )

        # Add movie to playlist
        playlist = Playlist.objects.get(id=playlist_id, user=request.user)
        playlist.movies.add(movie)
        messages.success(request,"Movie added to playlist successfully")
        return render(request, "temps/Search.html")

def fetch_movie_details(imdb_id):
    api_url = f"http://www.omdbapi.com/?apikey=97d611c7&i={imdb_id}"
    response = requests.get(api_url)
    return response.json()

@login_required
def user_playlists(request):
    playlists = Playlist.objects.filter(user=request.user)
    return render(request, 'temps/user_playlists.html', {'playlists': playlists})


@login_required
def movie_details(request, imdb_id):
    # Fetch movie details from an external API (like OMDB API)
    response = requests.get(f'http://www.omdbapi.com/?i={imdb_id}&apikey=97d611c7&s')
    movie_data = response.json()

    if 'Error' in movie_data:
        return render(request, 'movie_not_found.html', {'imdb_id': imdb_id})

    return render(request, 'temps/movie_details.html', {'movie': movie_data})

@login_required
def delete_playlist(request, playlist_id):
    try:
        playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
        playlist.delete()
        message = ''
        messages.error(request, 'Playlist deleted successfully.')
        return redirect('/playlists')
    except Exception as e:
        return redirect('/playlists')

def public_playlists(request):
    public_playlists = Playlist.objects.filter(is_public=True)
    return render(request, 'temps/public_playlists.html', {'public_playlists': public_playlists})


@login_required
def get_playlist_movies(request, playlist_id):
    # Fetch the playlist object
    playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
    # Get all movies associated with the playlist
    movies = playlist.movies.all()
    # Pass the playlist name and movies to the template context
    return render(request, 'temps/playlist_movies.html', {'playlist': playlist,'playlist_id': playlist_id, 'movies': movies})


def public_playlist_movies(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id, is_public=True)
    movies = playlist.movies.all()
    return render(request, 'temps/public_playlist_movies.html', {'playlist': playlist, 'movies': movies})

@login_required()
def toggle_privacy(request, playlist_id):
    if request.method == 'POST':
        playlist = get_object_or_404(Playlist, id=playlist_id)
        playlist.is_public = not playlist.is_public
        playlist.save()
        messages.success(request, 'Playlist privacy toggled successfully.')
    else:
        messages.error(request, 'Invalid request method.')
    return redirect('/playlists')  # or your desired redirect URL