from pydantic import BaseModel, Field


class CreateComment(BaseModel):
    user_id: int = Field(..., ge=1)         # id пользователя
    movie_id: int = Field(..., ge=1)        # id фильма
    text: str = Field(..., min_length=1)    # текст комментария
    created_at: int = Field(ge=0)                  # дата создания комментария (время Unix)


if __name__ == "__main__":
    pass
