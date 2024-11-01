import pytest
import requests
from utils.user_helpers import create_user, delete_user
from config import USER_ORDERS_URL, LOGIN_USER_URL


class TestGetUserOrders:

    @pytest.fixture
    def authorized_user(self):
        """Фикстура для создания и получения токена авторизованного пользователя."""
        user_data = {
            "email": "authorized_user@example.com",
            "password": "password123",
            "name": "Authorized User"
        }
        token, _ = create_user(user_data["email"], user_data["password"], user_data["name"])
        yield token  # Возвращаем токен для использования в тестах
        delete_user(token)  # Удаляем пользователя после завершения тестов

    def test_get_user_orders_authorized(self, authorized_user):
        """Тест получения заказов для авторизованного пользователя."""
        headers = {"Authorization": authorized_user}
        response = requests.get(USER_ORDERS_URL, headers=headers)

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert response.json().get("success") is True, "Request should be successful"
        assert "orders" in response.json(), "Response should contain 'orders'"
        assert isinstance(response.json().get("orders"), list), "'orders' should be a list"

    def test_get_user_orders_unauthorized(self):
        """Тест получения заказов без авторизации."""
        response = requests.get(USER_ORDERS_URL)

        assert response.status_code == 401, f"Expected 401, got {response.status_code}"
        assert response.json().get("success") is False, "Request should not be successful"
        assert response.json().get("message") == "You should be authorised", "Unexpected error message"
