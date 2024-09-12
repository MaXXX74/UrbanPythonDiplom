from django.db import models
from django.contrib.auth.models import User  # импорт модели пользователя
import time
import datetime


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
        ordering = ['name']  # сортировка по названию фильма

    def __str__(self):
        return f"{self.name} ({self.year})"


class Shots(models.Model):
    file = models.TextField(null=False,        verbose_name='Название файла-скриншота')
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE, related_name='shots', verbose_name='Фильм')
    url = models.TextField(verbose_name='Полный URL для файла-скриншота')

    class Meta:
        verbose_name = "Скриншот"
        verbose_name_plural = "Скриншоты"

    def __str__(self):
        return self.file


class Comments(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE, related_name='user_comments', verbose_name='Пользователь')
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE, related_name='movie_comments', verbose_name='Фильм')
    text = models.TextField(null=False, verbose_name='Комментарий')
    created_at = models.IntegerField(null=False, default=int(time.time()), verbose_name='Дата создания')

    def text_short(self):
        # обрезаем текст до 50 символов и добавляем многоточие
        return (self.text[:65] + '...') if len(self.text) > 65 else self.text

    def created_at_formatted(self):
        return datetime.datetime.fromtimestamp(self.created_at).strftime('%d-%m-%Y %H:%M:%S')

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return f'{self.user.username}: {self.text[:20]}'
