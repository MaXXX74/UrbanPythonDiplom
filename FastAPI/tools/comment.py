"""
Модуль с дополнительными функциями для работы с комментариями к фильму/сериалу
"""

import re, html


# подготавливает комментарий из формы для загрузки в БД
def get_comment_for_db(comment: str) -> str:
    """
    Функция подготавливает текст комментария из формы к загрузке в БД.

    Функция выполняет следующие действия для обработки текста комментария:
    - Удаляет лишние пробелы в начале и конце.
    - Убирает HTML-теги из текста.
    - Экранирует специальные символы для защиты от XSS-атак.

    Args:
        comment (str): текст комментария.

    Returns:
        str: Очищенный и отформатированный текст.
    """
    cleaned_comment = comment.strip()
    cleaned_comment = re.sub(r'<.*?>', '', cleaned_comment)
    cleaned_comment = html.escape(cleaned_comment)
    return cleaned_comment


# подготавливает комментарий для загрузки в шаблон
def get_comment_for_html(comment: str) -> str:
    """
    Функция подготавливает текст комментария загруженного из БД к размещению на HTML-странице.

    Функция выполняет следующие действия для обработки текста комментария:
    - Удаляет лишние пробелы в начале и конце.
    - Убирает HTML-теги из текста.
    - Экранирует специальные символы для защиты от XSS-атак.
    - Заменяет каждый перевод строки на тег <br>.

    Args:
        comment (str): текст комментария.

    Returns:
        str: Очищенный и отформатированный текст.
    """
    cleaned_comment = comment.strip()
    cleaned_comment = re.sub(r'<.*?>', '', cleaned_comment)
    cleaned_comment = html.escape(cleaned_comment)
    cleaned_comment = re.sub(r'\r\n', '<br>', cleaned_comment)
    return cleaned_comment

