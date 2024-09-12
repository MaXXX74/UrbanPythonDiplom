from django.http import HttpResponseRedirect
from django.db.models import F
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *
from .database import DBase
from .tools import get_comment_for_html, get_comment_for_db, sec_to_datetime

menu = [
    {"label": "Каталог", "link": "/"},
    {"label": "Поиск", "link": "#", "id": "search_button"}
]


# обработчик ошибки 404
def custom_404(request, exception):
    context = {
        'title': "Нет данных",
        'menu': menu,
    }
    return render(request, "nodata.html", context=context, status=404)


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
    try:
        movie = Movies.objects.values().get(id=id)
        shots = Shots.objects.values().filter(movie=id)
        comments = (Comments.objects
                    .filter(movie_id=id)                    # фильтр по movie_id
                    .select_related('user')                 # выполняем JOIN с моделью User
                    .order_by('-created_at')                # сортировка по created_at DESC
                    .values('user__first_name', 'text', 'created_at'))

        # приводим поля к соответствию шаблону
        for comment in comments:
            comment["user"] = comment["user__first_name"]
            comment["text"] = get_comment_for_html(comment["text"])
            comment["created_at"] = sec_to_datetime(comment["created_at"])

        context = {
            'title': "Карточка фильма",
            'menu': menu,
            'movie': movie,
            'shots': shots,
            'comments': comments,
            'link': "/page/",
        }
        return render(request, "movie.html", context=context)
    except Exception:
        context = {
            'title': "Нет данных",
            'menu': menu,
        }
        return render(request, "nodata.html", context=context)


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
    

def add_comment(request):
    movie_id = 0    # по умолчанию
    try:
        user_id = request.POST.get('user_id')
        movie_id = request.POST.get('movie_id')
        comment_text = get_comment_for_db(request.POST.get('text'))
        if comment_text:
            user = User.objects.get(id=user_id)
            movie = Movies.objects.get(id=movie_id)
            Comments.objects.create(
                user=user,
                movie=movie,
                text=comment_text,
                created_at=int(time.time())
            )
    except Exception:
        pass
    finally:
        # перезагружаем текущую страницу в любом случае
        return redirect(reverse('movie_page', args=[movie_id]))
