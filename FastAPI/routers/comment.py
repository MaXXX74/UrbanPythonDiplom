from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from backend.db_depends import get_db
from typing import Annotated
from models.user import User
from models.movie import Movie
from models.comment import Comment
from schemas.comment import CreateComment
from sqlalchemy import insert, select, update, delete
import time


comment = APIRouter(prefix="/json/comment", tags=["comment"])


# получение всех комментариев
@comment.get("/")
async def all_comments(db: Annotated[Session, Depends(get_db)]):
    """
    Получение всех комментариев из базы данных.
    """
    comments = db.scalars(select(Comment)).all()
    if comments is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There are no comments'
        )
    return comments


# получение комментария
@comment.get("/comment_id")
async def comment_by_id(db: Annotated[Session, Depends(get_db)], comment_id: int):
    """
    Получение информации о комментарии по его ID.

    - **comment_id**: ID комментария.
    """
    comment_value = db.scalar(select(Comment).where(Comment.id == comment_id))
    if comment_value is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Comment was not found'
        )
    return comment_value


# добавление комментария
@comment.post("/add")
async def add_comment(db: Annotated[Session, Depends(get_db)], new_comment: CreateComment):
    """
    Добавление нового комментария.

    - **user_id**: ID пользователя, оставившего комментарий.
    - **movie_id**: ID фильма, к которому оставлен комментарий.
    - **text**: Текст комментария.
    """
    # проверяем наличие пользователя от имени которого создается комментарий
    user_id = new_comment.user_id
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
        )

    # проверяем наличие фильма для которого создается комментарий
    movie_id = new_comment.movie_id
    movie = db.scalar(select(Movie).where(Movie.id == movie_id))
    if movie is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Movie was not found'
        )

    # добавляем комментарий для этого фильма
    db.execute(insert(Comment).values(
        user_id=new_comment.user_id,
        movie_id=new_comment.movie_id,
        text=new_comment.text,
        created_at=int(time.time())
    ))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }


# обновление комментария
@comment.put("/update")
async def update_comment(db: Annotated[Session, Depends(get_db)], comment_id: int, refresh_comment: CreateComment):
    """
    Обновление комментария по ID.

    - **comment_id**: ID комментария, который нужно обновить.
    - **user_id**: ID пользователя, обновившего комментарий.
    - **movie_id**: ID фильма, к которому принадлежит комментарий.
    - **text**: новый текст комментария.
    """
    # проверяем наличие комментария перед обновлением
    comment_value = db.scalar(select(Comment).where(Comment.id == comment_id))
    if comment_value is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Comment was not found'
        )
    db.execute(update(Comment).where(Comment.id == comment_id).values(
        user_id=refresh_comment.user_id,
        movie_id=refresh_comment.movie_id,
        text=refresh_comment.text,
        created_at=int(time.time())
    ))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Comment update is successful!'
    }


# удаление комментария
@comment.delete("/delete")
async def delete_comment(db: Annotated[Session, Depends(get_db)], comment_id: int):
    """
    Удаление комментария по ID.

    - **comment_id**: ID комментария, который нужно удалить.
    """
    # проверяем наличие комментария перед удалением
    comment_value = db.scalar(select(Comment).where(Comment.id == comment_id))
    if comment_value is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Comment was not found'
        )
    db.execute(delete(Comment).where(Comment.id == comment_id))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Comment was deleted successful!'
    }
