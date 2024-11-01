import pytest
import requests
from utils.generate_random_email import generate_random_email
from utils.user_helpers import create_user, delete_user
from config import REGISTER_USER_URL

@pytest.fixture
def unique_user_data():
    """Генерирует данные для уникального пользователя."""
    return {
        "email": generate_random_email(),
        "password": "password123",
        "name": "Unique User"
    }

@pytest.fixture
def existing_user_data():
    """Создает и возвращает данные существующего пользователя."""
    user_data = {
        "email": generate_random_email(),
        "password": "password123",
        "name": "Existing User"
    }
    token, _ = create_user(user_data['email'], user_data['password'], user_data['name'])
    yield user_data
    delete_user(token)

class TestUserRegistration:
    def test_create_unique_user(self, unique_user_data):
        """Тест для создания уникального пользователя"""
        response = requests.post(REGISTER_USER_URL, json=unique_user_data)

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert response.json().get("success") is True, "User creation failed"

        # Cleanup
        token = response.json().get("accessToken")
        delete_user(token)

    def test_create_existing_user(self, existing_user_data):
        """Тест для создания уже зарегистрированного пользователя"""
        response = requests.post(REGISTER_USER_URL, json=existing_user_data)

        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
        assert response.json().get("success") is False
        assert response.json().get("message") == "User already exists", "Unexpected error message"

    def test_create_user_missing_field(self):
        """Тест для создания пользователя с отсутствующим обязательным полем"""
        user_data = {
            "email": generate_random_email(),
            "password": "password123"
            # Поле "name" пропущено
        }

        response = requests.post(REGISTER_USER_URL, json=user_data)
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
        assert response.json().get("success") is False
        assert response.json().get("message") == "Email, password and name are required fields", "Unexpected error message"
