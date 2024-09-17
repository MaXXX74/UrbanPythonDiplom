"""
Модуль для работы с базой данных фильмов
"""

import sqlite3
import re


def is_float(s: str) -> bool:
    """
    Проверяет, можно ли преобразовать строку в число с плавающей точкой.

    Args:
        s (str): строка для проверки

    Returns:
        bool: True, если строку можно преобразовать в float, иначе False.
    """
    try:
        float(s)
        return True
    except ValueError:
        return False


def check_or_in_field(value: str) -> bool:
    """
    Проверяет, содержит ли строка ключевые слова "или" или "or".

    Args:
        value (str): строка для проверки.

    Returns:
        bool: True, если строка содержит "или" или "or" в любом регистре, иначе False.
    """
    or_lst = [" или ", " or "]
    value = value.lower()
    for item in or_lst:
        if item in value:
            return True
    return False


def check_and_in_field(value: str) -> bool:
    """
    Проверяет, содержит ли строка ключевые слова "и" или "and".

    Args:
        value (str): строка для проверки.

    Returns:
        bool: True, если строка содержит "и" или "and" в любом регистре, иначе False.
    """
    or_lst = [" и ", " and "]
    value = value.lower()
    for item in or_lst:
        if item in value:
            return True
    return False


def get_or_in_field(key: str, value: str) -> str:
    """
    Формирует SQL-запрос с условием "OR" для поля.

    Args:
        key (str): Имя поля.
        value (str): Значение для проверки.

    Returns:
        str: SQL-запрос с условием "OR".
    """
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


def get_and_in_field(key: str, value: str) -> str:
    """
    Формирует SQL-запрос с условием "AND" для поля.

    Args:
        key (str): имя поля.
        value (str): значение для проверки.

    Returns:
        str: SQL-запрос с условием "AND".
    """
    fields = re.split(r"(?: и | and | И | AND )", value)
    or_lst = list()
    for field in fields:
        field = field.strip()
        or_lst.append(f"{key} LIKE '%{field}%'")
    result = " AND ".join(or_lst)
    return f"({result})"


class DBase:
    """
    Класс для работы с базой данных SQLite.

    Attributes:
        __conn (sqlite3.Connection): подключение к базе данных.
        __cursor (sqlite3.Cursor): курсор для выполнения SQL-запросов.
    """

    def __init__(self, path="movies.db"):
        """
        Инициализация класса DBase с подключением к базе данных SQLite.

        Args:
            path (str): путь к файлу базы данных.
        """
        self.__conn = sqlite3.connect(path)
        self.__cursor = sqlite3.Cursor(self.__conn)
        self.__cursor.row_factory = sqlite3.Row

    def delete_tables(self):
        """
        Удаляет таблицы из базы данных фильмов, если они существуют.
        """
        sql = '''DROP TABLE IF EXISTS users;
                 DROP TABLE IF EXISTS movies;
                 DROP TABLE IF EXISTS shots;
                 DROP TABLE IF EXISTS comments;
              '''
        self.__cursor.executescript(sql)

    def create_tables(self):
        """
        Создает таблицы в базе данных, если они еще не существуют.
        """
        sql = '''CREATE TABLE users(
            id INTEGER NOT NULL,
            login VARCHAR(50) NOT NULL,
            name VARCHAR(50) NOT NULL,
            password_hash VARCHAR(64) NOT NULL,
            PRIMARY KEY (id)
            );

            CREATE TABLE movies (
            id INTEGER NOT NULL,
            name TEXT NOT NULL,
            ori_name TEXT NOT NULL,
            year INTEGER NOT NULL,
            poster TEXT NOT NULL,
            genre TEXT NOT NULL,
            creators TEXT NOT NULL,
            director TEXT NOT NULL,
            actors TEXT NOT NULL,
            description TEXT NOT NULL,
            rating_imdb FLOAT,
            rating_kinopoisk FLOAT,
            PRIMARY KEY (id)
            );

        CREATE TABLE shots (
            id INTEGER NOT NULL,
            file TEXT NOT NULL,
            movie_id INTEGER NOT NULL,
            url TEXT NOT NULL,
            PRIMARY KEY (id),
            FOREIGN KEY(movie_id) REFERENCES movies (id)
            );

        CREATE TABLE comments (
            id INTEGER NOT NULL,
            user_id INTEGER,
            movie_id INTEGER NOT NULL,
            text TEXT NOT NULL,
            created_at INTEGER NOT NULL,
            PRIMARY KEY (id),
            FOREIGN KEY(movie_id) REFERENCES movies (id),
            FOREIGN KEY(user_id) REFERENCES users (id)
            );
        '''
        self.__cursor.executescript(sql)

    def add_movie(self, movie: dict):
        """
        Добавляет фильм в базу данных.

        Args:
            movie (dict): словарь с данными о фильме.
        """
        if movie:
            sql = """INSERT INTO movies (name, ori_name, year, poster, genre, creators, director, actors, description, rating_imdb, rating_kinopoisk)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
            self.__cursor.execute(sql, (
                movie["name"],
                movie["ori_name"],
                movie["year"],
                movie["poster"],
                movie["genre"],
                movie["creators"],
                movie["director"],
                movie["actors"],
                movie["description"],
                movie["rating_imdb"],
                movie["rating_kinopoisk"]
            ))
            self.__conn.commit()
        else:
            print("Ошибка добавления фильма в БД")

    def get_movies_for_index_page(self, page: int = 1, args: dict = None):
        """
        Получает список фильмов для отображения на главной странице.

        Args:
            page (int): номер страницы.
            args (dict): фильтры для поиска фильмов.

        Returns:
            list, dict: список фильмов и информация о навигации по страницам.
        """
        CARDS_ON_PAGE = 8
        sql = "SELECT id, name, ori_name, year, poster FROM movies"
        fields = ['name', 'ori_name', 'year', 'genre', 'creators', 'director', 'actors', 'description', 'rating_imdb',
                  'rating_kinopoisk']
        if args is not None:
            where_lst = list()
            for key, value in args.items():
                if key in fields and value:
                    value = value.strip() if isinstance(value, str) else value
                    if key.startswith("rating"):
                        if is_float(value):
                            condition = f"{key} >= {value}"
                            where_lst.append(condition)
                    else:
                        if key == 'name' or key == 'ori_name':
                            condition = f"{key} LIKE '%{value}%'"
                        elif check_or_in_field(value):
                            condition = get_or_in_field(key, value)
                        elif check_and_in_field(value):
                            condition = get_and_in_field(key, value)
                        else:
                            condition = f"{key} LIKE '%{value}%'"
                        where_lst.append(condition)
            if where_lst:
                sql += " WHERE " + " AND ".join(where_lst)

        skip_recs = (page - 1) * CARDS_ON_PAGE
        sql += f" ORDER BY year DESC, rating_imdb DESC LIMIT {CARDS_ON_PAGE} OFFSET {skip_recs};"
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

        pages = {"previous": page - 1 if page > 1 else None, "next": page + 1 if len(result) == CARDS_ON_PAGE else None}
        return result, pages

    def get_movie_by_id(self, id: int):
        """
        Получает данные о фильме по его ID.

        Args:
            id (int): id фильма.

        Returns:
            sqlite3.Row: подробная информация о фильме.
        """
        sql = "SELECT * FROM movies WHERE id = ?"
        self.__cursor.execute(sql, (id,))
        return self.__cursor.fetchone()

    def get_shots_by_id(self, id: int):
        """
        Получает скриншоты по ID фильма.

        Args:
            id (int): id фильма.

        Returns:
            list: список скриншотов.
        """
        sql = "SELECT file, url FROM shots WHERE movie_id = ?"
        self.__cursor.execute(sql, (id,))
        return self.__cursor.fetchall()

    def get_comments(self, movie_id: int = None):
        """
        Возвращает список комментариев к фильму.

        Args:
            movie_id (int): id фильма (опционально).

        Returns:
            list: список комментариев.
        """
        sql = """SELECT name AS user, text, created_at FROM comments INNER JOIN users ON user_id = users.id """
        if movie_id is not None:
            sql += "WHERE movie_id = ? ORDER BY created_at DESC"

        self.__cursor.execute(sql, (movie_id,) if movie_id else None)
        comments = self.__cursor.fetchall()
        result = [{
            "user": comment["user"],
            "text": get_comment_for_html(comment["text"]),          # подготавливаем комментарий для вывода HTML
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
            created_at = time.time()
        if movie_id is None or text.strip() == "":
            return

        sql = """INSERT INTO comments (user_id, movie_id, text, created_at) VALUES (?, ?, ?, ?)"""
        self.__cursor.execute(sql, (user_id, movie_id, text, created_at))
        self.__conn.commit()

    def is_exist(self, table_name: str, field_name: str, value) -> bool:
        """
            Проверяет, существует ли запись в таблице базы данных с указанным значением в заданном поле.

            Метод выполняет SQL-запрос для поиска записи в таблице `table_name`,
            где значение в поле `field_name` соответствует заданному `value`.
            Возвращает `True`, если такая запись существует, и `False`, если запись не найдена.

            Args:
                table_name (str): Название таблицы, в которой выполняется поиск.
                field_name (str): Название поля, в котором выполняется поиск значения.
                value: Значение, которое проверяется на наличие в таблице.

            Returns:
                bool: `True`, если запись найдена, `False` в противном случае.
       """
        sql = f"SELECT 1 FROM {table_name} WHERE {field_name} = ? LIMIT 1"
        self.__cursor.execute(sql, (value,))
        return bool(self.__cursor.fetchone())