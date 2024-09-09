"""
Модуль для работы с базой данных
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# создаем движок для работы с базой данных SQLite
engine = create_engine('sqlite:///movies.db', echo=True)
# создаем фабрику сессий для взаимодействия с базой данных
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    """
    Базовый класс для всех моделей SQLAlchemy.
    """
    pass

