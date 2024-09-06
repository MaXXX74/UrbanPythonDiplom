from pydantic import BaseModel, Field


class CreateComment(BaseModel):
    user_id: int = Field(..., ge=1)         # id пользователя
    movie_id: int = Field(..., ge=1)        # id фильма
    text: str = Field(..., min_length=1)    # текст комментария
    created_at: int = Field()                      # дата создания комментария


if __name__ == "__main__":
    pass
    # s = "some string"
    # print(s.find('z'))
    #


