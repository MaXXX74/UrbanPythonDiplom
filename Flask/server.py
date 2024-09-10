from flask import Flask, render_template, request, session, redirect, url_for
from database import DBase
import re, html

app = Flask(__name__)
app.secret_key = 'hdggrtt465673728kgjj6'

menu = [
    {"label": "Каталог", "link": "/"},
    {"label": "Поиск", "link": "#", "id": "search_button"}
]


# очищает текст комментария
def clean_comment(comment: str) -> str:
    """
    Очищает и форматирует текст комментария.

    Функция выполняет следующие действия для обработки текста комментария:
    - Удаляет лишние пробелы в начале и конце строки.
    - Убирает HTML-теги из текста.
    - Экранирует специальные символы для защиты от XSS-атак.
    - Заменяет последовательные переводы строки на тег <br>.
    - Сокращает несколько пробелов до одного.

    Args:
        comment (str): Текст комментария.

    Returns:
        str: Очищенный и отформатированный текст.
    """
    cleaned_comment = comment.strip()
    cleaned_comment = re.sub(r'<.*?>', '', cleaned_comment)
    cleaned_comment = html.escape(cleaned_comment)
    cleaned_comment = re.sub(r'(\r\n)+', '<br>', cleaned_comment)
    cleaned_comment = re.sub('r\n+', '<br>', cleaned_comment)
    cleaned_comment = re.sub(r'\s+', ' ', cleaned_comment)
    return cleaned_comment


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
    db = DBase()
    user_id = request.form.get('user_id')
    movie_id = request.form.get('movie_id')
    text = clean_comment(request.form.get('text'))
    if text and text != "<br>":
        db.add_comment(user_id=user_id, movie_id=movie_id, text=text)
    return redirect(url_for('movie_page', id=movie_id))


if __name__ == "__main__":
    app.run(debug=True)
