import pytest
import requests
from utils.user_helpers import create_user, delete_user
from utils.generate_random_email import generate_random_email
from config import LOGIN_USER_URL

@pytest.fixture
def registered_user():
    """Фикстура для создания и последующего удаления пользователя с уникальным email."""
    email = generate_random_email()
    password = "password123"
    name = "Test User"
    token, user_data = create_user(email, password, name)
    yield user_data  # Возвращаем данные пользователя для тестов
    delete_user(token)  # Удаляем пользователя после тестов

class TestLoginUser:
    def test_login_existing_user(self, registered_user):
        """Тест успешного входа для существующего пользователя."""
        response = requests.post(LOGIN_USER_URL, json={
            "email": registered_user["email"],
            "password": registered_user["password"]
        })
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert response.json().get("success") is True, "Login failed"
        assert "accessToken" in response.json(), "accessToken not returned"
        assert "refreshToken" in response.json(), "refreshToken not returned"

    def test_login_invalid_credentials(self):
        """Тест неуспешного входа с неверными логином и паролем."""
        response = requests.post(LOGIN_USER_URL, json={
            "email": "nonexistent@example.com",
            "password": "wrongpassword"
        })
        assert response.status_code == 401, f"Expected 401, got {response.status_code}"
        assert response.json().get("success") is False, "Login should have failed"
        assert response.json().get("message") == "email or password are incorrect", "Unexpected error message"
