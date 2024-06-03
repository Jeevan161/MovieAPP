"""movieapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [

    path('create_playlist', views.create_playlist, name="create_playlist"),
    path('get_playlists', views.get_playlists, name="get_playlists"),
    path('add_to_playlist', views.add_to_playlist, name="add_to_playlist"),
    path('playlists', views.user_playlists, name='user_playlists'),
    path('movie/<str:imdb_id>/', views.movie_details, name='movie_details'),
    path('delete/<str:imdb_id>/<int:playlist_id>/', views.delete_mv, name='delete_mv'),
    path('playlist/<int:playlist_id>/', views.get_playlist_movies, name='get_playlist_movies'),
    path('delete_playlist/<int:playlist_id>', views.delete_playlist, name='delete_playlist'),
    path('public_playlists/', views.public_playlists, name='public_playlists'),
    path('public_playlist/<int:playlist_id>/', views.public_playlist_movies, name='public_playlist_movies'),
    path('toggle_privacy/<int:playlist_id>/', views.toggle_privacy, name='toggle_privacy'),

]
