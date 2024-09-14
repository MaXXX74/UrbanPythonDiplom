"""
Основной модуль для запуска web-сервера на Flask.

Команда запуска из корня проекта: python server.py
"""

from flask import Flask, render_template, request, session, redirect, url_for
from database import DBase
from forms.add_comment import AddCommentForm
from tools.comment import get_comment_for_db
from tools.user import get_current_user_id

app = Flask(__name__)
app.secret_key = 'hdggrtt465673728kgjj6'

menu = [
    {"label": "Каталог", "link": "/"},
    {"label": "Поиск", "link": "#", "id": "search_button"}
]


# обработчик ошибки 404
@app.errorhandler(404)
def page_not_found(e):
    """
    Обрабатывает ошибку 404 (страница не найдена)

    Возвращает HTML-страницу с заголовком "Нет данных".

    Args:
        e: исключение 404.

    Returns:
        str: сгенерированная HTML-страница по шаблону.
    """
    context = {
        "title": "Нет данных",
        "menu": menu,
    }
    return render_template("nodata.html", **context), 404


# страницы каталога
@app.route("/page/<int:page>/")
@app.route("/")
def index_page(page=1):
    """
    Возвращает страницу каталога фильмов.

    Возвращает список фильмов с пагинацией, отображая до 8 фильмов на странице.
    Если фильмы отсутствуют, возвращается страница с сообщением "Нет данных".

    Args:
        page (int): номер страницы каталога (по умолчанию 1).

    Returns:
        str: сгенерированная HTML-страница, содержащая список фильмов или переход
        на страницу с сообщением, что данные отсутствуют.
    """
    db = DBase()
    movies_lst, pages = db.get_movies_for_index_page(page=page)

    # если список фильмов не пуст
    if len(movies_lst) > 0:
        context = {
            "title": "Каталог фильмов",
            "menu": menu,
            "movies": movies_lst,
            "pages": pages,
            "link": "/page/"
        }
        return render_template("index.html", **context)
    else:
        # если данные отсутствуют
        context = {
            "title": "Нет данных",
            "menu": menu,
        }
        return render_template("nodata.html", **context)


# страницы с результатами поиска
@app.route("/search/page/<int:page>/")
@app.route("/search/", methods=['GET', 'POST'])
def search_page(page=1):
    """
    Возвращает страницу каталога фильмов с учетом поиска.

    Принимает поисковые параметры через GET-запрос и отображает результаты на основе
    параметров поиска. Также поддерживает пагинацию.

    Args:
        page (int): номер страницы с результатами поиска (по умолчанию 1).

    Returns:
        str: возвращает HTML-страницу с результатами поиска или страницу с
        заголовком, что данные отсутствуют.
    """
    # если были переданы параметры - сохраняем их
    if request.args:
        session["last_request"] = request.args
    last_request = session.get("last_request", None)

    db = DBase()
    movies_lst, pages = db.get_movies_for_index_page(args=last_request, page=page)

    # если список фильмов не пуст
    if len(movies_lst) > 0:
        context = {
            "title": "Результат поиска",
            "menu": menu,
            "movies": movies_lst,
            "pages": pages,
            "link": "/search/page/"
        }
        return render_template("index.html", **context)
    else:
        # если данные отсутствуют
        context = {
            "title": "Нет данных",
            "menu": menu,
        }
        return render_template("nodata.html", **context)


# страница с информацией о фильме
@app.route("/movie/<int:id>/")
def movie_page(id: int):
    """
    Возвращает страницу с подробной информацией о фильме

    Отображает информацию о фильме, его кадры и комментарии. Если фильм не найден,
    возвращает сообщение "Нет данных".

    Args:
        id (int): ID фильма.

    Returns:
        str: возвращает HTML-страницу с информацией о фильме или страницу с заголовком,
        что данные отсутствуют.
    """
    db = DBase()
    movie = db.get_movie_by_id(id)
    shots = db.get_shots_by_id(id)
    comments = db.get_comments(movie_id=id)
    if movie:
        context = {
            "menu": menu,
            "movie": movie,
            "shots": shots,
            "comments": comments,
        }
        return render_template("movie.html", **context)
    else:
        context = {
            "title": "Нет данных",
            "menu": menu,
        }
        return render_template("nodata.html", **context)


# обработка добавления нового комментария
@app.route("/comment/add/", methods=['POST'])
def add_comment():
    """
    Обработчик добавления комментария.

    Принимает данные формы POST-запроса и добавляет новый комментарий к фильму.
    После добавления перенаправляет пользователя на страницу фильма.

    Returns:
        Redirect: перенаправление на страницу фильма после добавления комментария.
    """
    form = AddCommentForm(request.form)
    if request.method == 'POST' and form.validate():

        # если валидация прошла, можно получить данные и сохранить их
        db = DBase()
        user_id = get_current_user_id()
        movie_id = form.movie_id.data
        text = get_comment_for_db(form.text.data)

        try:
            if (db.is_exist("users", "id", user_id)
                    and db.is_exist("movies", "id", movie_id)):
                db.add_comment(user_id=user_id, movie_id=movie_id, text=text)
        except Exception as e:
            print(f"ERROR: ошибка добавления комментария. {e}")
        finally:
            return redirect(url_for('movie_page', id=movie_id))

    # в случае ошибки - возвращаемся на главную страницу
    return redirect(url_for('index_page'))


if __name__ == "__main__":
    app.run(debug=True)
