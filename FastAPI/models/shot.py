from backend.db import Base
from sqlalchemy import Column, Integer, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from models import *


class Shot(Base):
    __tablename__ = 'shots'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    file = Column(Text, nullable=False)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    url = Column(Text, nullable=False)

    # обратная связь с моделью Movie
    movie = relationship("Movie", back_populates="shots")


if __name__ == "__main__":
    from sqlalchemy.schema import CreateTable
    print(CreateTable(Shot.__table__))
