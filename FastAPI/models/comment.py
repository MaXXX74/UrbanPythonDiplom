"""
Модель SQLAlchemy комментариев к фильмам
"""

from backend.db import Base
from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from models import *


class Comment(Base):
    """
    Модель SQLAlchemy комментариев к фильмам.

    Представляет собой комментарий пользователя к конкретному фильму.
    Связан с моделью `User` (пользователь) и моделью `Movie` (фильм).

    Attributes:
        id (int): уникальный идентификатор комментария.
        user_id (int, nullable): идентификатор пользователя, оставившего комментарий. Связь с таблицей `users`.
        movie_id (int): идентификатор фильма, к которому оставлен комментарий. Связь с таблицей `movies`.
        text (str): текст комментария.
        created_at (int): время создания комментария в формате UNIX timestamp.
        user (relationship): связь "много к одному" с моделью `User`. Один пользователь может иметь много комментариев.
        movie (relationship): связь "много к одному" с моделью `Movie`. Один фильм может иметь много комментариев.
    """

    __tablename__ = 'comments'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    text = Column(Text, nullable=False)
    created_at = Column(Integer, nullable=False)

    # связь с моделью User: много комментариев - один пользователь
    user = relationship("User", back_populates="comments", single_parent=True)

    # связь с моделью Movie: много комментариев - один фильм
    movie = relationship("Movie", back_populates="comments", single_parent=True)


if __name__ == "__main__":
    from sqlalchemy.schema import CreateTable

    # вывод SQL-выражения для создания таблицы `comments`
    print(CreateTable(Comment.__table__))
