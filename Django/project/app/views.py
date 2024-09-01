from django.shortcuts import render
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
    movie = Movies.objects.values().get(id=id)
    shots = Shots.objects.values().filter(movie=id)
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


def search_page(request, page=1):
    # если были получены GET-параметры поиска, сохраняем их
    if request.GET:
        request.session["last_request"] = dict(request.GET)
    last_request = request.session.get("last_request", None)

    db = DBase()
    movies_lst, pages = db.get_movies_for_index_page(args=last_request, page=page)
    if len(movies_lst) > 0:
        context = {
            'title': "Результат поиска",
            'menu': menu,
            'movies': movies_lst,
            'pages': pages,
            'link': "/search/page/",
        }
        return render(request, "index.html", context=context)
    else:
        context = {
            'title': "Нет данных",
            'menu': menu,
            'pages': pages,
            'link': "/search/page/",
        }
        return render(request,"nodata.html", context=context)