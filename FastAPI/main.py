"""
Основной модуль для запуска web-сервера на FastAPI.

Команда запуска из корня проекта: python -m uvicorn main:app
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
import secrets
from tools.database import DBase

app = FastAPI()

# пути для шаблонов и статическим файлам
templates = Jinja2Templates(directory="templates")                          # путь к директории с шаблонами
app.mount("/static", StaticFiles(directory="static"), name="static")   # путь к статическим файлам

# подготовка для работы с сессиями
secret_key = secrets.token_hex(32)                                          # генерация безопасного secret_key
app.add_middleware(SessionMiddleware, secret_key=secret_key)                # middleware для работы с сессиями

# элементы верхнего меню
menu = [
    {"label": "Каталог", "link": "/"},
    {"label": "Поиск", "link": "#", "id": "search_button"}
]


@app.get("/", response_class=HTMLResponse)
@app.get("/page/{page}", response_class=HTMLResponse)
async def index_page(request: Request, page: int = 1):
    """
    Возвращает страницу каталога фильмов.

    Параметры:
        request (Request): текущий запрос FastAPI.
        page (int, опционально): номер страницы для пагинации (по умолчанию 1).

    Возвращает:
        HTMLResponse: сгенерированная HTML-страница, содержащая список фильмов или
        переход на страницу с сообщением, что данные отсутствуют.
    """
    db = DBase()
    movies_lst, pages = db.get_movies_for_index_page(page=page)

    # если список фильмов не пуст
    if len(movies_lst) > 0:
        template_file = "index.html"
        context = {
            "request": request,
            "title": "Каталог фильмов",
            "menu": menu,
            "movies": movies_lst,
            "pages": pages,
            "link": "/page/",
        }
    else:
        # если данные отсутствуют
        template_file = "nodata.html"
        context = {
            "request": request,
            "title": "Нет данных",
            "menu": menu,
            "pages": pages,
            "link": "/page/",
        }
    return templates.TemplateResponse(template_file, context=context)


@app.get("/search/page/{page}", response_class=HTMLResponse)
@app.get("/search/", response_class=HTMLResponse)
async def search_page(request: Request, page: int = 1):
    """
    Возвращает страницу каталога фильмов с учетом поиска.

    Параметры:
        request (Request): текущий запрос FastAPI.
        page (int, опционально): номер страницы для пагинации (по умолчанию 1).

    Возвращает:
        HTMLResponse: сгенерированная HTML-страница, содержащая список фильмов с учетом поиска или
        переход на страницу с сообщением, что данные отсутствуют.
    """
    query_params = dict(request.query_params)

    # если были переданы параметры - сохраняем их
    if query_params:
        request.session['last_request'] = query_params
    last_request = request.session.get("last_request", None)

    db = DBase()
    movies_lst, pages = db.get_movies_for_index_page(args=last_request, page=page)

    # если список фильмов не пуст
    if len(movies_lst) > 0:
        template_file = "index.html"
        context = {
            "request": request,
            "title": "Результат поиска",
            "menu": menu,
            "movies": movies_lst,
            "pages": pages,
            "link": "/search/page/",
        }
    else:
        # если данные отсутствуют
        template_file = "nodata.html"
        context = {
            "request": request,
            "title": "Нет данных",
            "menu": menu,
            "pages": pages,
            "link": "/search/page/",
        }
    return templates.TemplateResponse(template_file, context=context)


@app.get("/movie/{id}", response_class=HTMLResponse)
async def movie_page(request: Request, id: int):
    """
    Возвращает страницу с подробной информацией о фильме

    Параметры:
        request (Request): текущий запрос FastAPI.
        id (int): идентификатор фильма в БД (поле movie.id)

    Возвращает:
        HTMLResponse: сгенерированная HTML-страница, с информацией о фильме или
        переход на страницу с сообщением, что данные отсутствуют.
    """
    db = DBase()
    movie = db.get_movie_by_id(id)
    shots = db.get_shots_by_id(id)
    comments = db.get_comments(movie_id=id)

    # если список фильмов не пуст
    if movie:
        template_file = "movie.html"
        context = {
            "request": request,
            "menu": menu,
            "movie": movie,
            "shots": shots,
            "comments": comments,
        }
    else:
        # если данные отсутствуют
        template_file = "nodata.html"
        context = {
            "request": request,
            "title": "Нет данных",
            "menu": menu,
            "pages": (None, None),
        }
    return templates.TemplateResponse(template_file, context=context)
