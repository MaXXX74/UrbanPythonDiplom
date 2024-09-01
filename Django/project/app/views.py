from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
# from .forms import ContactForm
from .models import *
from .database import DBase

menu = [
    {"label": "Каталог", "link": "/"},
    {"label": "Поиск", "link": "#", "id": "search_button"}
]


def index_page(request, page=1):
    db = DBase()
    movies_lst, pages = db.get_movies_for_index_page(page=page)
    if len(movies_lst) > 0:
        context = {
            'title': "Каталог фильмов",
            'menu': menu,
            'movies': movies_lst,
            'pages': pages,
            'link': "/page/",
        }
        return render(request, "index.html", context=context)
    else:
        context = {
            'title': "Нет данных",
            'menu': menu,
            'pages': pages,
            'link': "/page/",
        }
        return render(request, "nodata.html", context=context)


def movie_page(request, id: int):
    db = DBase()
    movie = db.get_movie_by_id(id)
    shots = db.get_shots_by_id(id)
    if movie:
        context = {
            'title': "Каталог фильмов",
            'menu': menu,
            'movie': movie,
            'shots': shots,
            # 'link': "/page/",
        }
        return render(request,"movie.html", context=context)
    else:
        context = {
            'title': "Нет данных",
            'menu': menu,
            'pages': (None, None),
            # 'link': "/page/",
        }
        return render(request,"nodata.html", context=context)
