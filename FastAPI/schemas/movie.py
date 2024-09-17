from pydantic import BaseModel, Field


class CreateMovie(BaseModel):
    name: str = Field(..., min_length=1,        description="название на русском языке")
    ori_name: str = Field(..., min_length=1,    description="название на языке оригинала")
    year: int = Field(..., ge=1,                description="год создания")
    poster: str = Field(..., min_length=1,      description="название файла-постера")
    genre: str = Field(..., min_length=1,       description="жанры через запятую")
    creators: str = Field(..., min_length=1,    description="страна производитель и кинокомпания")
    director: str = Field(..., min_length=1,    description="ФИО режиссера")
    actors: str = Field(..., min_length=1,      description="основные актеры через запятую")
    description: str = Field(..., min_length=1, description="краткое описание фильма")
    rating_imdb: float = Field(default=None, ge=0,     description="рейтинг IMDB")
    rating_kinopoisk: float = Field(default=None, ge=0,description="рейтинг IMDB")

