import pytest
import requests
from utils.generate_random_email import generate_random_email
from config import UPDATE_USER_URL, REGISTER_USER_URL

class TestUpdateUser:

    @pytest.fixture
    def authorized_user(self):
        """Фикстура для создания пользователя и получения токена авторизации."""
        user_data = {
            "email": generate_random_email(),
            "password": "password123",
            "name": "Authorized User"
        }
        response = requests.post(REGISTER_USER_URL, json=user_data)
        assert response.status_code == 200, f"Failed to create user: {response.status_code}"
        token = response.json().get("accessToken")
        yield token, user_data
        headers = {"Authorization": token}
        requests.delete(UPDATE_USER_URL, headers=headers)

    def test_update_user_with_authorization(self, authorized_user):
        """Тест изменения данных пользователя с авторизацией."""
        token, user_data = authorized_user
        updated_data = {
            "email": generate_random_email(),
            "name": "Updated Name"
        }
        headers = {"Authorization": token}
        response = requests.patch(UPDATE_USER_URL, json=updated_data, headers=headers)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert response.json().get("success") is True, "User data update failed"
        response_data = response.json().get("user")
        for key, value in updated_data.items():
            if key == "email":
                assert response_data[key].lower() == value.lower(), f"Expected {key} to be {value}, got {response_data[key]}"
            else:
                assert response_data[key] == value, f"Expected {key} to be {value}, got {response_data[key]}"

    def test_update_user_without_authorization(self):
        """Тест изменения данных пользователя без авторизации, ожидаем ошибку."""
        updated_data = {
            "email": generate_random_email(),
            "name": "Updated Name"
        }
        response = requests.patch(UPDATE_USER_URL, json=updated_data)
        assert response.status_code == 401, f"Expected 401, got {response.status_code}"
        assert response.json().get("success") is False, "Expected failure for unauthorized update"
        assert response.json().get("message") == "You should be authorised", "Unexpected error message"

    def test_update_single_field_with_authorization(self, authorized_user):
        """Тест изменения одного поля (имя) с авторизацией."""
        token, user_data = authorized_user
        updated_data = {"name": "New Name"}
        headers = {"Authorization": token}
        response = requests.patch(UPDATE_USER_URL, json=updated_data, headers=headers)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert response.json().get("success") is True, "User data update failed"
        response_data = response.json().get("user")
        assert response_data["name"] == updated_data["name"], f"Expected name to be {updated_data['name']}, got {response_data['name']}"

    def test_update_multiple_fields_with_authorization(self, authorized_user):
        """Тест изменения нескольких полей (почта и имя) с авторизацией."""
        token, user_data = authorized_user
        updated_data = {
            "email": generate_random_email(),
            "name": "Another Name"
        }
        headers = {"Authorization": token}
        response = requests.patch(UPDATE_USER_URL, json=updated_data, headers=headers)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert response.json().get("success") is True, "User data update failed"
        response_data = response.json().get("user")
        assert response_data["email"].lower() == updated_data["email"].lower(), f"Expected email to be {updated_data['email']}, got {response_data['email']}"
        assert response_data["name"] == updated_data["name"], f"Expected name to be {updated_data['name']}, got {response_data['name']}"
