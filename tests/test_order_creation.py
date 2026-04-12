import allure
import pytest
from config.config import BASE_URL, EXPECTED_STATUS_CODES
from helpers.api_helpers import post_request


@allure.feature("Создание заказа")
class TestOrderCreation:

    @pytest.mark.parametrize("color", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"]
    ])
    @allure.title("Создание заказа с цветом: {color}")
    def test_order_creation_with_color(self, created_courier_id, color):
        payload = {
            "courierId": created_courier_id,
            "color": color
        }
        response = post_request(f"{BASE_URL}/orders", payload)
        assert response.status_code == EXPECTED_STATUS_CODES['order_creation_success']
        response_json = response.json()
        assert response_json.get("color") == color

    @allure.title("Создание заказа без указания цвета")
    def test_order_creation_without_color(self, created_courier_id):
        payload = {
            "courierId": created_courier_id
            # color не передаём
        }
        response = post_request(f"{BASE_URL}/orders", payload)
        assert response.status_code == EXPECTED_STATUS_CODES['order_creation_success']
        response_json = response.json()
        # API должен вернуть color как пустой массив
        assert response_json.get("color") == []