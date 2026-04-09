import allure
import pytest
from config.config import BASE_URL, EXPECTED_STATUS_CODES
from helpers.api_helpers import post_request


@allure.feature("Создание заказа")
class TestOrderCreation:

    @pytest.mark.parametrize("color", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        []
    ])
    @allure.title("Создание заказа с цветом: {color}")
    def test_order_creation_with_different_colors(self, created_courier_id, color):
        # Условия удалены — используем payload напрямую
        payload = {
            "courierId": created_courier_id,
            "color": color
        }
        # Если цвет пустой, можно не передавать (API должен принять)
        if not color:
            del payload["color"]

        response = post_request(f"{BASE_URL}/orders", payload)
        assert response.status_code == EXPECTED_STATUS_CODES['order_creation_success']
        response_json = response.json()

        assert "track" in response_json
        assert isinstance(response_json["track"], int)
        assert "orderId" in response_json
        assert isinstance(response_json["orderId"], int)

        # Проверяем цвет, если он был в запросе
        if "color" in payload:
            assert response_json.get("color") == payload["color"]
        else:
            # Если цвет не передавали, он может быть пустым или отсутствовать
            assert response_json.get("color") == []