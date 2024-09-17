from pydantic import BaseModel, Field


class CreateComment(BaseModel):
    user_id: int = Field(..., ge=1,         description="id пользователя")
    movie_id: int = Field(..., ge=1,        description="id фильма")
    text: str = Field(..., min_length=1,    description="текст комментария")
