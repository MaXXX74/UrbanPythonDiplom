from django.contrib import admin
from .models import *


@admin.register(Movies)
class MoviesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year', 'genre', 'creators', 'director', 'rating_imdb', 'rating_kinopoisk')
    search_fields = ('name', 'genre', 'creators', 'director', 'actors')
    list_filter = ('year', 'director', 'rating_imdb', 'rating_kinopoisk')


@admin.register(Shots)
class ShotsAdmin(admin.ModelAdmin):
    list_display = ('movie', 'file', 'url')
    list_filter = ('movie',)
