import allure
import pytest
from config import BASE_URL, EXPECTED_STATUS_CODES
from helpers.api_helpers import post_request

@allure.feature("Создание заказа")
class TestOrderCreation:

    @pytest.fixture
    def courier_id(self, courier_data):
        """Фикстура для получения ID курьера"""
        courier = courier_data()
        assert courier is not None

        payload = {
            "login": courier["login"],
            "password": courier["password"]
        }
        response = post_request(f"{BASE_URL}/login", payload)
        return response.json()["id"]

    @pytest.mark.parametrize("color", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        []
    ])
    @allure.title("Создание заказа с цветом: {color}")
    @allure.story("Создание заказа с разными вариантами цвета")
    def test_order_creation_with_different_colors(self, courier_id, color):
        payload = {"courierId": courier_id}
        if color:
            payload["color"] = color

        response = post_request(f"{BASE_URL}/orders", payload)
        assert response.status_code == EXPECTED_STATUS_CODES['order_creation_success']
        response_json = response.json()

        # Проверяем обязательные поля в ответе
        assert "track" in response_json
        assert isinstance(response_json["track"], int)
        assert "orderId" in response_json
        assert isinstance(response_json["orderId"], int)

        # Если цвет был указан, проверяем его сохранение
        if color:
            assert "color" in response_json
            assert response_json["color"] == color
        else:
            # Если цвет не указан, он может отсутствовать или быть пустым
            if "color" in response_json:
                assert response_json["color"] == []