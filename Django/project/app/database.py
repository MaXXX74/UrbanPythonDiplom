import sqlite3
import re
import time
from app.tools import get_comment_for_html, sec_to_datetime


def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def check_or_in_field(value):
    or_lst = [" или ", " or "]
    value = value.lower()
    for item in or_lst:
        if item in value:
            return True
    return False


def check_and_in_field(value):
    or_lst = [" и ", " and "]
    value = value.lower()
    for item in or_lst:
        if item in value:
            return True
    return False


def get_or_in_field(key, value):
    fields = re.split(r"(?: или | or | ИЛИ | OR )", value)
    or_lst = list()
    for field in fields:
        field = field.strip()
        if check_and_in_field(field):
            or_lst.append(get_and_in_field(key, field))
        else:
            or_lst.append(f"{key} LIKE '%{field}%'")
    result = " OR ".join(or_lst)
    return f"({result})"


def get_and_in_field(key, value):
    fields = re.split(r"(?: и | and | И | AND )", value)
    or_lst = list()
    for field in fields:
        field = field.strip()
        or_lst.append(f"{key} LIKE '%{field}%'")
    result = " AND ".join(or_lst)
    return f"({result})"


class DBase:
    def __init__(self):
        self.__conn = sqlite3.connect("movies.db")
        self.__cursor = sqlite3.Cursor(self.__conn)
        self.__cursor.row_factory = sqlite3.Row

    def get_movies_for_index_page(self, page=1, args=None):
        CARDS_ON_PAGE = 8  # число карточек на одной странице
        sql = "SELECT id, name, ori_name, year, poster FROM app_movies"
        fields = ['name', 'ori_name', 'year', 'genre', 'creators', 'director', 'actors', 'description', 'rating_imdb',
                  'rating_kinopoisk']
        if args is not None:
            args = {key: value[0] for key, value in args.items()}       # корректировка формата аргументов
            where_lst = list()
            for key, value in args.items():
                if key in fields and value:
                    if isinstance(value, str):  # убираем пробелы в начале и конце значения параметра
                        value = value.strip()
                    if key.startswith("rating"):                        # рейтинги обрабатываем по-особому
                        if is_float(value):
                            condition = f"{key} >= {value}"
                            where_lst.append(condition)
                    else:                                               # иначе это обычное поле
                        if key == 'name' or key == 'ori_name':          # для названий условия не проверяем
                            condition = f"{key} LIKE '%{value}%'"
                        elif check_or_in_field(value):                  # для остальных проверяем, есть ли ИЛИ
                            condition = get_or_in_field(key, value)
                        elif check_and_in_field(value):                 # или условие И
                            condition = get_and_in_field(key, value)
                        else:                                           # или в поле обычный текст
                            condition = f"{key} LIKE '%{value}%'"
                        where_lst.append(condition)
            if len(where_lst) > 0:                                      # если собрали условия - добавляем в запрос
                where_str = " WHERE " + " AND ".join(where_lst)
                sql += where_str

        # сколько пропускаем записей при переходе по страницам
        skip_recs = (page - 1) * CARDS_ON_PAGE

        sql += f" ORDER BY rating_imdb DESC LIMIT {CARDS_ON_PAGE} OFFSET {skip_recs};"
        # print(sql)
        self.__cursor.execute(sql)
        movies = self.__cursor.fetchall()
        
        result = []
        for movie in movies:
            changed_movie = {
                "id": movie["id"],
                "poster": movie["poster"],
                "caption": f"{movie['name']} / {movie['ori_name']} / {movie['year']}" if movie["name"] != movie[
                    "ori_name"]
                else f"{movie['name']} / {movie['year']}"
            }
            result.append(changed_movie)

        # определяем предыдущие и последующие страницы для навигации
        pages = {"previous": None, "next": None}
        if page > 1:
            pages["previous"] = page - 1
        if len(result) == CARDS_ON_PAGE:
            pages["next"] = page + 1

        return result, pages

    def get_comments(self, movie_id: int = None):
            """
            Возвращает список комментариев к фильму.

            Args:
                movie_id (int): id фильма (опционально).

            Returns:
                list: список комментариев.
            """
            sql = """SELECT first_name AS user_name, text, created_at FROM app_comments 
            INNER JOIN auth_user ON user_id = auth_user.id """
            if movie_id is not None:
                sql += "WHERE movie_id = ? ORDER BY created_at DESC"

            self.__cursor.execute(sql, (movie_id,) if movie_id else None)
            comments = self.__cursor.fetchall()

            result = [
                {"user": comment["user_name"],
                 "text": get_comment_for_html(comment["text"]),
                 "created_at": sec_to_datetime(comment["created_at"])
                 }
                for comment in comments]
            return result

    def add_comment(self, user_id: int = None, movie_id: int = None, text: str = "", created_at: int = None):
        """
        Добавляет комментарий к фильму.

        Args:
            user_id (int): id пользователя.
            movie_id (int): id фильма.
            text (str): текст комментария.
            created_at (int): время создания комментария (опционально, по умолчанию текущее время).
        """
        if created_at is None:
            created_at = int(time.time())
        if movie_id is None or text.strip() == "":
            return

        sql = """INSERT INTO app_comments (user_id, movie_id, text, created_at) VALUES (?, ?, ?, ?)"""
        self.__cursor.execute(sql, (user_id, movie_id, text, created_at))
        self.__conn.commit()


if __name__ == "__main__":
    db = DBase()
    # res = db.get_comments(movie_id=2)
    # print(res)
    db.add_comment(user_id=1, movie_id=2, text='Это 2-й комментарий на фильм &quot;Черное солнце&quot')
