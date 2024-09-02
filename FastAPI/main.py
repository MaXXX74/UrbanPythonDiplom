from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
import secrets
from database import DBase

app = FastAPI()

# пути для шаблонов и статическим файлам
templates = Jinja2Templates(directory="templates")                          # путь к директории с шаблонами
app.mount("/static", StaticFiles(directory="static"), name="static")   # путь к статическим файлам

# подготовка для работы с сессиями
secret_key = secrets.token_hex(32)                                          # генерация безопасного secret_key
app.add_middleware(SessionMiddleware, secret_key=secret_key)                # middleware для работы с сессиями


menu = [
    {"label": "Каталог", "link": "/"},
    {"label": "Поиск", "link": "#", "id": "search_button"}
]


@app.get("/", response_class=HTMLResponse)
@app.get("/page/{page}", response_class=HTMLResponse)
async def index_page(request: Request, page: int = 1):
    db = DBase()
    movies_lst, pages = db.get_movies_for_index_page(page=page)
    if len(movies_lst) > 0:
        context = {
            "request": request,
            "title": "Каталог фильмов",
            "menu": menu,
            "movies": movies_lst,
            "pages": pages,
        }
        template_file = "index.html"
    else:
        context = {
            "request": request,
            "title": "Нет данных",
            "menu": menu,
            "pages": pages,
        }
        template_file = "nodata.html"
    return templates.TemplateResponse(template_file, context=context)


@app.get("/search/page/{page}", response_class=HTMLResponse)
@app.get("/search/", response_class=HTMLResponse)
async def search_page(request: Request, page: int = 1):
    query_params = dict(request.query_params)
    if query_params:
        request.session['last_request'] = query_params
    last_request = request.session.get("last_request", None)

    db = DBase()
    movies_lst, pages = db.get_movies_for_index_page(args=last_request, page=page)
    if len(movies_lst) > 0:
        context = {
            "request": request,
            "title": "Результат поиска",
            "menu": menu,
            "movies": movies_lst,
            "pages": pages,
            "source": "search",
        }
        template_file = "index.html"
    else:
        context = {
            "request": request,
            "title": "Нет данных",
            "menu": menu,
            "pages": pages,
            "source": "search",
        }
        template_file = "nodata.html"
    return templates.TemplateResponse(template_file, context=context)


@app.get("/movie/{id}")
def movie_page(request: Request, id: int):
    db = DBase()
    movie = db.get_movie_by_id(id)
    shots = db.get_shots_by_id(id)
    if movie:
        context = {
            "request": request,
            "menu": menu,
            "movie": movie,
            "shots": shots,
        }
        template_file = "movie.html"
    else:
        context = {
            "request": request,
            "title": "Нет данных",
            "menu": menu,
            "pages": (None, None),
        }
        template_file = "nodata.html"
    return templates.TemplateResponse(template_file, context=context)
