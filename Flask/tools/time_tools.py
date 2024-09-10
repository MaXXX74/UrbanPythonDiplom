"""
Модуль для дополнительной работы с датой и временем
"""

import time
import datetime
from typing import Optional


def sec_to_datetime(sec: Optional[int | str] = None, fmt: str = '%d/%m/%Y %H:%M:%S') -> str:
    """
    Преобразует количество секунд с начала эпохи Unix в отформатированную строку с датой и временем.

    Параметры:
        sec (Optional[int], опционально): кол-во секунд с начала эпохи Unix. По умолчанию используется текущее время.
        fmt (str, опционально): формат вывода даты и времени в формате strftime. По умолчанию '%d/%m/%Y %H:%M:%S'.

    Возвращает:
        str: отформатированная строка с датой и временем.

    Исключения:
        ValueError: если параметр `sec` не может быть преобразован в целое число.

    Пример:
        >>> sec_to_datetime(1633065600)
        '01/10/2021 08:20:00'

        >>> sec_to_datetime(sec='1725492668', fmt='%Y/%m/%d %H:%M:%S')
        '2024/09/05 02:31:08'
    """

    if sec is None:
        sec = int(time.time())           # используем текущее время, если sec не указано
    try:
        sec = int(sec)              # проверка корректности преобразования
    except (TypeError, ValueError):
        raise ValueError("Параметр 'sec' должен быть целым числом или None.")

    return datetime.datetime.fromtimestamp(sec).strftime(fmt)
