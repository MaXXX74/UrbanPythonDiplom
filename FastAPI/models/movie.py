from backend.db import Base
from sqlalchemy import Column, Integer, Text, Float
from sqlalchemy.orm import relationship
from models import *


class Movie(Base):
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
    shots = relationship("Shot", back_populates="movie", cascade="all, delete-orphan")


if __name__ == "__main__":
    from sqlalchemy.schema import CreateTable
    print(CreateTable(Movie.__table__))
