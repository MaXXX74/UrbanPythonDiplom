from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from backend.db_depends import get_db
from typing import Annotated
from models.user import Movie
from models.shot import Shot
from schemas.shot import CreateShot
from sqlalchemy import insert, select, update, delete


shot = APIRouter(prefix="/json/shot", tags=["shot"])


# получение всех скриншотов
@shot.get("/")
async def all_shots(db: Annotated[Session, Depends(get_db)]):
    """
    Получение информации о всех скриншотах.
    """
    shots = db.scalars(select(Shot)).all()
    if shots is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There are no screenshots'
        )
    return shots


# получение информации по скриншоту
@shot.get("/shot_id")
async def shot_by_id(db: Annotated[Session, Depends(get_db)], shot_id: int):
    """
    Получение информации о скриншоте по его ID.

    - **shot_id**: ID скриншота.
    """
    shot_value = db.scalar(select(Shot).where(Shot.id == shot_id))
    if shot_value is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Screenshot was not found'
        )
    return shot_value


# добавление нового скриншота
@shot.post("/add")
async def add_shot(db: Annotated[Session, Depends(get_db)], new_shot: CreateShot):
    """
    Добавление нового скриншота.

    - **file**: Название файла скриншота.
    - **movie_id**: ID фильма, к которому принадлежит скриншот.
    - **url**: URL файла скриншота.
    """
    # проверяем наличие фильма
    movie_id = new_shot.movie_id
    movie = db.scalar(select(Movie).where(Movie.id == movie_id))
    if movie is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Movie was not found'
        )

    # добавляем скриншот для этого фильма
    db.execute(insert(Shot).values(
        file=new_shot.file,
        movie_id=new_shot.movie_id,
        url=new_shot.url,
    ))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }


# обновление существующего скриншота
@shot.put("/update")
async def update_shot(db: Annotated[Session, Depends(get_db)], shot_id: int, refresh_shot: CreateShot):
    """
    Обновление существующего скриншота.

    - **shot_id**: ID скриншота, который нужно обновить.
    - **file**: Название файла скриншота.
    - **movie_id**: ID фильма, к которому принадлежит скриншот.
    - **url**: URL файла скриншота.
    """
    # проверяем наличие скриншота
    shot_value = db.scalar(select(Shot).where(Shot.id == shot_id))
    if shot_value is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Screenshot was not found'
        )
    db.execute(update(Shot).where(Shot.id == shot_id).values(
        file=refresh_shot.file,
        movie_id=refresh_shot.movie_id,
        url=refresh_shot.url,
    ))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Screenshot update is successful!'
    }


# удаление скриншота
@shot.delete("/delete")
async def delete_shot(db: Annotated[Session, Depends(get_db)], shot_id: int):
    """
    Удаление скриншота.

    - **shot_id**: ID скриншота, который нужно удалить.
    """
    # проверяем наличие скриншота
    shot_value = db.scalar(select(Shot).where(Shot.id == shot_id))
    if shot_value is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Screenshot was not found'
        )
    db.execute(delete(Shot).where(Shot.id == shot_id))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Screenshot was deleted successful!'
    }
