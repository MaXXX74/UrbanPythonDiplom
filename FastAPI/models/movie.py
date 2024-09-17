"""
Модель SQLAlchemy c информацией о фильмах
"""

from backend.db import Base
from sqlalchemy import Column, Integer, Text, Float
from sqlalchemy.orm import relationship
from models import *


class Movie(Base):
    """
    Модель SQLAlchemy c информацией о фильмах.

    Содержит информацию о фильмах, включая их название, год выпуска, постер, жанр, и рейтинги.
    Связан с моделью `Shot` (скриншоты).

    Attributes:
        id (int): уникальный идентификатор фильма. Является первичным ключом.
        name (str): название фильма.
        ori_name (str): оригинальное название фильма.
        year (int): год выпуска фильма.
        poster (str): ссылка на изображение постера фильма.
        genre (str): жанр фильма.
        creators (str): список создателей фильма (например, сценаристы, продюсеры).
        director (str): имя режиссёра фильма.
        actors (str): список главных актёров фильма.
        description (str): описание сюжета фильма.
        rating_imdb (float, optional): рейтинг фильма на IMDb (может быть `None`).
        rating_kinopoisk (float, optional): рейтинг фильма на Кинопоиске (может быть `None`).
        shots (relationship): отношение с моделью Shot. Один фильм может иметь несколько скриншотов.
    """

    __tablename__ = 'movies'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    ori_name = Column(Text, nullable=False)
    year = Column(Integer, nullable=False)
    poster = Column(Text, nullable=False)
    genre = Column(Text, nullable=False)
    creators = Column(Text, nullable=False)
    director = Column(Text, nullable=False)
    actors = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    rating_imdb = Column(Float, nullable=True)
    rating_kinopoisk = Column(Float, nullable=True)

    # связь с моделью Shot: один фильм - много скриншотов
    shots = relationship("Shot", back_populates="movie", cascade="all")

    # связь с моделью Comment: один фильм - много комментариев
    comments = relationship("Comment", back_populates="movie", cascade="all")


if __name__ == "__main__":
    from sqlalchemy.schema import CreateTable

    # вывод SQL-выражения для создания таблицы `movies`
    print(CreateTable(Movie.__table__))
