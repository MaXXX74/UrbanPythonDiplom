from django.db import models


class Movies(models.Model):
    id = models.IntegerField(primary_key=True,  verbose_name='ID')
    name = models.TextField(null=False,         verbose_name='Название')
    ori_name = models.TextField(null=False,     verbose_name="Название ориг.")
    year = models.IntegerField(null=False,      verbose_name='Год выпуска')
    poster = models.TextField(null=False,       verbose_name='Файл-постер')
    genre = models.TextField(null=False,        verbose_name='Жанры')
    creators = models.TextField(null=False,     verbose_name='Создатели')
    director = models.TextField(null=False,     verbose_name='Режиссер')
    actors = models.TextField(null=False,       verbose_name='Актеры')
    description = models.TextField(null=False,  verbose_name='Описание')
    rating_imdb = models.FloatField(            verbose_name='IMDB')
    rating_kinopoisk = models.FloatField(       verbose_name='Кинопоиск')

    class Meta:
        verbose_name = "Фильм/сериал"
        verbose_name_plural = "Фильмы/сериалы"

    def __str__(self):
        return f"{self.name} ({self.year})"


class Shots(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name='ID')
    file = models.TextField(null=False,        verbose_name='Название файла-скриншота')
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE, related_name='shots', verbose_name='Фильм')
    url = models.TextField(verbose_name='Полный URL для файла-скриншота')

    class Meta:
        verbose_name = "Скриншот"
        verbose_name_plural = "Скриншоты"

    def __str__(self):
        return self.file