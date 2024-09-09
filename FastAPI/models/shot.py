"""
Модель SQLAlchemy для таблицы скриншотов
"""

from backend.db import Base
from sqlalchemy import Column, Integer, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from models import *


class Shot(Base):
    """
    Модель SQLAlchemy для таблицы скриншотов.

    Таблица хранит данные о скриншотах фильмов, включая путь к файлу, URL и связь с фильмом.
    Связан с моделью `Movie` (фильм).

    Attributes:
        id (int): уникальный идентификатор скриншота. Является первичным ключом.
        file (str): путь к файлу скриншота.
        movie_id (int): идентификатор фильма, к которому относится скриншот. Ссылается на таблицу "movies".
        url (str): URL для доступа к скриншоту.
        movie (Movie): связь с моделью Movie, указывающая, к какому фильму относится данный скриншот.
    """

    __tablename__ = 'shots'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    file = Column(Text, nullable=False)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    url = Column(Text, nullable=False)

    # связь с моделью Movie: много скриншотов - один фильм
    movie = relationship("Movie", back_populates="shots")


if __name__ == "__main__":
    from sqlalchemy.schema import CreateTable

    # вывод SQL-выражения для создания таблицы `shots`
    print(CreateTable(Shot.__table__))
