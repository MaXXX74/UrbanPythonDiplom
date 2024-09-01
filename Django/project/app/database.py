import sqlite3
import re


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

    def delete_tables(self):
        # удаляем таблицы в БД если они есть
        sql = """DROP TABLE IF EXISTS app_movies;
                 DROP TABLE IF EXISTS app_shots;
              """
        self.__cursor.executescript(sql)

    def create_tables(self):
        sql = """CREATE TABLE app_movies(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            ori_name TEXT NOT NULL,
            year INTEGER NOT NULL,
            poster TEXT NOT NULL,
            genre TEXT NOT NULL,
            creators TEXT NOT NULL,
            director TEXT NOT NULL,
            actors TEXT NOT NULL,
            description TEXT NOT NULL,
            rating_imdb REAL,
            rating_kinopoisk REAL
        );
        """
        self.__cursor.execute(sql)

    def add_movie(self, movie):
        if movie:
            sql = """INSERT INTO app_movies (name, ori_name, year, poster, genre, creators, director, actors, description, rating_imdb, rating_kinopoisk) 
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
            )
                                  )
            self.__conn.commit()
        else:
            print("Ошибка добавления фильма в БД")

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
        result = list()
        for movie in movies:
            changed_movie = dict()
            changed_movie["id"], changed_movie["poster"] = movie["id"], movie["poster"]
            if movie["name"] == movie["ori_name"]:
                changed_movie["caption"] = f"{movie['name']} / {movie['year']}"
            else:
                changed_movie["caption"] = f"{movie['name']} / {movie['ori_name']} / {movie['year']}"
            result.append(changed_movie)

        # определяем предыдущие и последующие страницы для навигации
        pages = {"previous": None, "next": None}
        if page > 1:
            pages["previous"] = page - 1
        if len(result) == CARDS_ON_PAGE:
            pages["next"] = page + 1

        return result, pages

    def get_movie_by_id(self, id):
        sql = "SELECT * FROM app_movies WHERE id = ?"
        self.__cursor.execute(sql, (id,))
        return self.__cursor.fetchone()

    def get_shots_by_id(self, id):
        sql = "SELECT file, url FROM app_shots WHERE movie_id = ?"
        self.__cursor.execute(sql, (id,))
        return self.__cursor.fetchall()


if __name__ == "__main__":
    db = DBase()
    # movies = [
    #     {"name": "Холоп", "ori_name": "Холоп", "year": 2019, "poster": "poster_25.jpg",
    #      "genre": "комедия",
    #      "creators": "Россия, Yellow, Black & White",
    #      "director": "Клим Шипенко",
    #      "actors": "Милош Бикович, Александра Бортич, Александр Самойленко, Иван Охлобыстин, Мария Миронова мл., Олег Комаров (II), Ольга Дибцева, Кирилл Нагиев, Сергей Соцердотский, Софья Зайка",
    #      "description": "Молодой мажор Гриша заигрался в красивую жизнь и решил, что ему всё дозволено. Он натворил много дел, и теперь ему грозит тюрьма. Чтобы исправить своего сына, отчаявшийся отец-олигарх идёт на крайние меры. Вместе с психологом он придумывает уникальный проект: на базе заброшенной деревни воссоздаётся атмосфера России XIX века, а Гриша попадает в подстроенную аварию и якобы переносится в прошлое. На самом деле над ним проводится изощрённый психологический эксперимент — избалованного мажора превращают в обычного холопа Гришку, живущего в хлеву на территории барской усадьбы. Его окружают актёры, чья цель — изменить его жизнь и личность. За каждым его движением пристально следит команда психолога с помощью множества камер. Грише предстоит заново научиться общаться с людьми, ценить простые удовольствия, работать, а также обрести истинную любовь.",
    #      "rating_imdb": 6.7,
    #      "rating_kinopoisk": 7.1
    #     }
    # ]
    # for movie in movies:
    #     db.add_movie(movie)

