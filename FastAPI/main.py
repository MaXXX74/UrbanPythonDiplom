"""
Основной модуль для запуска web-сервера на FastAPI.

Команда запуска из корня проекта: python -m uvicorn main:app

Для запуска без допуска к документации swagger и пр. замените `app = FastAPI()` на
`app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)`

"""
from typing import Annotated

from fastapi import FastAPI, Request, status, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select, insert, exists, desc
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
import secrets
from tools.database import DBase
from tools.user import get_current_user_id
from tools.comment import get_comment_for_db, get_comment_for_html
from tools.time_tools import sec_to_datetime
from backend.db_depends import get_db
from models.comment import Comment
from models.user import User
from models.movie import Movie
from models.shot import Shot
from routers.movie import movie
from routers.shot import shot
from routers.comment import comment
import time

app = FastAPI()
# app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

# подключаем роутеры для API
app.include_router(movie)
app.include_router(shot)
app.include_router(comment)

# пути для шаблонов и статическим файлам
templates = Jinja2Templates(directory="templates")              # путь к директории с шаблонами
app.mount("/static", StaticFiles(directory="static"), name="static")  # путь к статическим файлам

# подготовка для работы с сессиями
secret_key = secrets.token_hex(32)                              # генерация безопасного secret_key
app.add_middleware(SessionMiddleware, secret_key=secret_key)    # middleware для работы с сессиями

# элементы верхнего меню
menu = [
    {"label": "Каталог", "link": "/"},
    {"label": "Поиск", "link": "#", "id": "search_button"}
]


# обработчик для ошибки 404
@app.exception_handler(StarletteHTTPException)
async def custom_404_handler(request: Request, exc: StarletteHTTPException):
    """
    Обрабатывает исключения HTTP, в частности ошибку 404 (Not Found).

    Этот обработчик проверяет статус ошибки и, если это ошибка 404, возвращает
    сгенерированный HTML-ответ с использованием шаблона "nodata.html". В противном случае,
    возвращает простое сообщение об ошибке с кодом ответа HTTP.

    Args:
        request (Request): Запрос, который привел к ошибке.
        exc (StarletteHTTPException): Исключение, содержащее информацию об ошибке HTTP.

    Returns:
        TemplateResponse или HTMLResponse: Возвращает HTML-ответ в случае ошибки 404,
        либо текстовый ответ для других HTTP-ошибок.

    Context (для шаблона):
        - request (Request): Объект запроса.
        - title (str): Заголовок страницы ("Нет данных").
        - menu (list): Меню, используемое для отображения на странице (пример).
        - pages (tuple): Пара для навигации по страницам (пример).

    Примеры ошибок:
        - Если статус код ошибки 404, возвращается страница с ошибкой, используя шаблон.
        - Для других ошибок возвращается сообщение с описанием ошибки.
    """
    if exc.status_code == 404:
        context = {
            "request": request,
            "title": "Нет данных",
            "menu": menu,
        }
        # возвращаем HTML-ответ с использованием шаблона "nodata.html"
        return templates.TemplateResponse("nodata.html", context=context, status_code=404)

    # для других ошибок возвращаем HTML-ответ с текстом ошибки
    return HTMLResponse(f"Error: {exc.detail}", status_code=exc.status_code)


# страницы каталога
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
        }
    return templates.TemplateResponse(template_file, context=context)


# страницы с результатами поиска
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
        }
    return templates.TemplateResponse(template_file, context=context)


# страница с информацией о фильме
@app.get("/movie/{id}", response_class=HTMLResponse)
async def movie_page(request: Request, db: Annotated[Session, Depends(get_db)], id: int):
    """
    Возвращает страницу с подробной информацией о фильме

    Параметры:
        request (Request): текущий запрос FastAPI.
        id (int): идентификатор фильма в БД (поле movie.id)

    Возвращает:
        HTMLResponse: сгенерированная HTML-страница, с информацией о фильме или
        переход на страницу с сообщением, что данные отсутствуют.
    """
    movie = db.scalar(select(Movie).where(Movie.id == id))
    if movie:
        shots = db.scalars(select(Shot).where(Shot.movie_id == id)).all()
        comments = (db.query(User.name, Comment.text, Comment.created_at)
                    .join(User)
                    .filter(Comment.movie_id == id)
                    .order_by(desc(Comment.created_at)
        ).all())

        # подготавливаем данные для загрузки в шаблон
        comments = [{
            "user": comment[0],
            "text": get_comment_for_html(comment[1]),  # подготавливаем комментарий для вывода HTML
            "created_at": sec_to_datetime(comment[2])
        }
            for comment in comments]

        # готовим контекст для шаблона
        template_file = "movie.html"
        context = {
            "request": request,
            "menu": menu,
            "movie": movie,
            "shots": shots,
            "comments": comments,
        }
    else:
        # если данные отсутствуют (фильм не найден)
        template_file = "nodata.html"
        context = {
            "request": request,
            "title": "Нет данных",
            "menu": menu,
        }
    return templates.TemplateResponse(template_file, context=context)


# обработка добавления нового комментария
@app.post("/comment/add/")
async def add_comment(
        db: Annotated[Session, Depends(get_db)],
        movie_id: int = Form(0),        # чтобы не было исключения
        text: str = Form("")):          # если поля отсутствуют
    """
    Обработчик добавления комментария.

    Принимает данные формы POST-запроса и добавляет новый комментарий к фильму.
    После добавления перенаправляет пользователя на страницу фильма.

    Returns:
        Redirect: перенаправление на страницу фильма после добавления комментария
        или на главную страницу каталога, если такой фильм отсутствует
    """
    # проверяем полученные данные
    if movie_id <= 0:
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    elif not text.strip():
        return RedirectResponse(url=f"/movie/{movie_id}", status_code=status.HTTP_303_SEE_OTHER)

    # если все нормально - добавляем данные
    user_id = get_current_user_id()         # получаем user_id текущего пользователя
    text = get_comment_for_db(text)         # готовим комментарий для загрузки в БД
    try:
        if (db.scalar(select(exists().where(User.id == user_id)))               # если user_id есть в БД
                and db.scalar(select(exists().where(Movie.id == movie_id)))):   # и movie_id тоже
            db.execute(insert(Comment).values(user_id=user_id, movie_id=movie_id, text=text, created_at=int(time.time())))
            db.commit()
    except Exception as e:
        print(f"ERROR: ошибка добавления комментария. {e}")
    finally:
        return RedirectResponse(url=f"/movie/{movie_id}", status_code=status.HTTP_303_SEE_OTHER)
