"""
Модель SQLAlchemy для таблицы пользователей
"""

from backend.db import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models import *


class User(Base):
    """
    Модель SQLAlchemy для таблицы пользователей.

    Таблица хранит информацию о пользователях, включая их логин, имя и хэш пароля.

    Attributes:
        id (int): уникальный идентификатор пользователя. Является первичным ключом.
        login (str): логин пользователя, длина до 50 символов.
        name (str): имя пользователя, длина до 50 символов.
        password_hash (str): хэш пароля пользователя, длина 64 символа.
        comments (list[Comment]): связь с моделью Comment, указывающая на список комментариев пользователя.
    """

    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String(length=50), nullable=False)
    name = Column(String(length=50), nullable=False)
    password_hash = Column(String(length=64), nullable=False)

    # связь с моделью Comment: один пользователь - много комментариев
    comments = relationship("Comment", back_populates="user", cascade="all")


if __name__ == "__main__":
    from sqlalchemy.schema import CreateTable

    # вывод SQL-выражения для создания таблицы `users`
    print(CreateTable(User.__table__))
