import pytest
import requests
from config import CREATE_ORDER_URL, LOGIN_USER_URL, INGREDIENTS_URL
from utils.user_helpers import create_user, delete_user
from utils.generate_random_email import generate_random_email

@pytest.fixture
def authorized_user():
    """Фикстура для создания авторизованного пользователя и получения токена."""
    user_data = {
        "email": generate_random_email(),
        "password": "password123",
        "name": "Order Test User"
    }
    token, _ = create_user(user_data['email'], user_data['password'], user_data['name'])
    yield token
    delete_user(token)

@pytest.fixture
def ingredient_ids():
    """Фикстура для получения валидных идентификаторов ингредиентов."""
    response = requests.get(INGREDIENTS_URL)
    assert response.status_code == 200, f"Failed to get ingredients: {response.status_code}"
    return [ingredient["_id"] for ingredient in response.json().get("data", [])]

class TestOrderCreation:

    def test_create_order_with_authorization(self, authorized_user, ingredient_ids):
        """Тест создания заказа с авторизацией и ингредиентами."""
        headers = {"Authorization": authorized_user}
        order_data = {"ingredients": ingredient_ids[:2]}  # Используем первые два ингредиента

        response = requests.post(CREATE_ORDER_URL, json=order_data, headers=headers)

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert response.json().get("success") is True, "Order creation failed"
        assert "order" in response.json(), "Order details missing in response"

    def test_create_order_without_authorization(self, ingredient_ids):
        """Тест создания заказа без авторизации, но с ингредиентами."""
        order_data = {"ingredients": ingredient_ids[:2]}

        response = requests.post(CREATE_ORDER_URL, json=order_data)

        assert response.status_code == 401, f"Expected 401, got {response.status_code}"
        assert response.json().get("success") is False, "Order should not be created without authorization"

    def test_create_order_with_ingredients(self, authorized_user, ingredient_ids):
        """Тест создания заказа с валидными ингредиентами."""
        headers = {"Authorization": authorized_user}
        order_data = {"ingredients": ingredient_ids[:2]}

        response = requests.post(CREATE_ORDER_URL, json=order_data, headers=headers)

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert response.json().get("success") is True, "Order creation failed"

    def test_create_order_without_ingredients(self, authorized_user):
        """Тест создания заказа с авторизацией, но без ингредиентов."""
        headers = {"Authorization": authorized_user}
        order_data = {"ingredients": []}  # Пустой список ингредиентов

        response = requests.post(CREATE_ORDER_URL, json=order_data, headers=headers)

        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
        assert response.json().get("success") is False, "Order should not be created without ingredients"
        assert response.json().get("message") == "Ingredient ids must be provided", "Unexpected error message"

    def test_create_order_with_invalid_ingredient_hash(self, authorized_user):
        """Тест создания заказа с неверным хешем ингредиента."""
        headers = {"Authorization": authorized_user}
        order_data = {"ingredients": ["invalid_ingredient_hash"]}

        response = requests.post(CREATE_ORDER_URL, json=order_data, headers=headers)

        assert response.status_code == 500, f"Expected 500, got {response.status_code}"
        assert response.json().get("success") is False, "Order creation should fail with invalid ingredient hash"
