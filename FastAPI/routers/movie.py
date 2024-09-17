from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from backend.db_depends import get_db
from typing import Annotated
from models.user import Movie
from models.shot import Shot
from models.comment import Comment
from schemas.movie import CreateMovie
from sqlalchemy import insert, select, update, delete


movie = APIRouter(prefix="/json/movie", tags=["movie"])


# получение всех фильмов
@movie.get("/")
async def all_movies(db: Annotated[Session, Depends(get_db)]):
    """
    Получение всех фильмов из базы данных.
    """
    movies = db.scalars(select(Movie)).all()
    if movies is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There are no movies'
        )
    return movies


# получение информации по фильму
@movie.get("/movie_id")
async def movie_by_id(db: Annotated[Session, Depends(get_db)], movie_id: int):
    """
    Получение информации о фильме по его ID.

    - **movie_id**: ID фильма.
    """
    movie_value = db.scalar(select(Movie).where(Movie.id == movie_id))
    if movie_value is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Movie was not found'
        )
    return movie_value


# получение скриншотов фильма
@movie.get("/movie_id/shots")
async def shots_by_movie_id(db: Annotated[Session, Depends(get_db)], movie_id: int):
    """
    Получение списка скриншотов для фильма по его ID.

    - **movie_id**: ID фильма.
    """
    # ищем фильм по movie_id
    movie_value = db.scalar(select(Movie).where(Movie.id == movie_id))
    if movie_value is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Movie was not found'
        )

    # нашли фильм - выводим скриншоты для него
    shots = db.scalars(select(Shot).where(Shot.movie_id == movie_id)).all()
    if shots is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'There are no shots for movie_id {movie_id}'
        )
    return shots


# получение комментариев фильма
@movie.get("/movie_id/comments")
async def comments_by_movie_id(db: Annotated[Session, Depends(get_db)], movie_id: int):
    """
    Получение списка комментариев для фильма по его ID.

    - **movie_id**: ID фильма.
    """
    # ищем фильм по movie_id
    movie_value = db.scalar(select(Movie).where(Movie.id == movie_id))
    if movie_value is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Movie was not found'
        )

    # нашли фильм - выводим комментарии для него
    comments = db.scalars(select(Comment).where(Comment.movie_id == movie_id)).all()
    if comments is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'There are no comments for movie_id {movie_id}'
        )
    return comments


# добавление фильма
@movie.post("/add")
async def add_movie(db: Annotated[Session, Depends(get_db)], new_movie: CreateMovie):
    """
    Добавление нового фильма в базу данных.

    - **name**: название фильма.
    - **ori_name**: оригинальное название фильма.
    - **year**: год выпуска фильма.
    - **poster**: постер фильма.
    - **genre**: жанр фильма.
    - **creators**: список создателей фильма.
    - **director**: режиссёр фильма.
    - **actors**: актёры фильма.
    - **description**: описание фильма.
    - **rating_imdb**: рейтинг IMDb.
    - **rating_kinopoisk**: рейтинг Кинопоиска.
    """
    db.execute(insert(Movie).values(
        name=new_movie.name,
        ori_name=new_movie.ori_name,
        year=new_movie.year,
        poster=new_movie.poster,
        genre=new_movie.genre,
        creators=new_movie.creators,
        director=new_movie.director,
        actors=new_movie.actors,
        description=new_movie.description,
        rating_imdb=new_movie.rating_imdb,
        rating_kinopoisk=new_movie.rating_kinopoisk
    ))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }


# обновление фильма
@movie.put("/update")
async def update_movie(db: Annotated[Session, Depends(get_db)], movie_id: int, refresh_movie: CreateMovie):
    """
    Обновление информации о фильме по его ID.

    - **movie_id**: ID фильма.
    """
    movie_value = db.scalar(select(Movie).where(Movie.id == movie_id))
    if movie_value is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Movie was not found'
        )
    db.execute(update(Movie).where(Movie.id == movie_id).values(
        name=refresh_movie.name,
        ori_name=refresh_movie.ori_name,
        year=refresh_movie.year,
        poster=refresh_movie.poster,
        genre=refresh_movie.genre,
        creators=refresh_movie.creators,
        director=refresh_movie.director,
        actors=refresh_movie.actors,
        description=refresh_movie.description,
        rating_imdb=refresh_movie.rating_imdb,
        rating_kinopoisk=refresh_movie.rating_kinopoisk
    ))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Movie update is successful!'
    }


# удаление фильма
@movie.delete("/delete")
async def delete_movie(db: Annotated[Session, Depends(get_db)], movie_id: int):
    """
    Удаление фильма по его ID.

    - **movie_id**: ID фильма.
    """
    movie_value = db.scalar(select(Movie).where(Movie.id == movie_id))
    if movie_value is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Movie was not found'
        )
    db.execute(delete(Shot).where(Shot.movie_id == movie_id))
    db.execute(delete(Comment).where(Comment.movie_id == movie_id))
    db.execute(delete(Movie).where(Movie.id == movie_id))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Movie was deleted successful!'
    }
