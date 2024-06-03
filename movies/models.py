from django.db import models
from django.contrib.auth.models import User


class Movie(models.Model):
    imdb_id = models.CharField(max_length=15, unique=True)
    mv_name = models.CharField(max_length=255, default=" ")
    mv_year = models.CharField(max_length=255, default=" ")
    mv_poster = models.CharField(max_length=455, default=" ")
    def __str__(self):
        return self.imdb_id


class Playlist(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlists')
    movies = models.ManyToManyField(Movie, related_name='playlists')
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.name
