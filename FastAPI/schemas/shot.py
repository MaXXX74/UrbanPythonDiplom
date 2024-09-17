from pydantic import BaseModel, Field


class CreateShot(BaseModel):
    file: str = Field(..., min_length=1,        description="название файла скриншота")
    movie_id: int = Field(..., ge=1,            description="id фильма-владельца скриншота")
    url: str = Field(..., min_length=1,         description="URL полноразмерного скриншота")
