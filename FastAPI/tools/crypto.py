"""

"""
import hashlib


def get_hash(passw: str) -> str:
    # создаем хеш пароля с использованием SHA-256
    hash_object = hashlib.sha256(passw.encode())
    return hash_object.hexdigest()


if __name__ == "__main__":
    password = input("Введите пароль для хеширования: ")
    hashed_password = get_hash(password)
    print(f"Хешированный пароль: '{hashed_password}'")

