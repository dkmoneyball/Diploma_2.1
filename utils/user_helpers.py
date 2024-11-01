import requests
from config import REGISTER_USER_URL, USER_INFO_URL


def create_user(email: str, password: str, name: str):
    """Создает нового пользователя и возвращает accessToken и user_data."""
    user_data = {
        "email": email,
        "password": password,
        "name": name
    }
    response = requests.post(REGISTER_USER_URL, json=user_data)
    if response.status_code != 200:
        raise Exception(f"Failed to create user: {response.json()}")

    token = response.json().get("accessToken")
    return token, user_data


def delete_user(token: str):
    """Удаляет пользователя по токену"""
    headers = {"Authorization": token}
    response = requests.delete(USER_INFO_URL, headers=headers)
    if response.status_code not in (200, 202):
        raise Exception(f"Failed to delete user: {response.status_code}")
