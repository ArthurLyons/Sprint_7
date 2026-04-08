import allure
from config import BASE_URL, EXPECTED_STATUS_CODES
from helpers.api_helpers import get_request

@allure.feature("Список заказов")
class TestOrdersList:

    @allure.title("Получение списка всех заказов")
    @allure.story("Получение списка заказов из системы")
    def test_get_orders_list(self):
        response = get_request(f"{BASE_URL}/orders")
        assert response.status_code == EXPECTED_STATUS_CODES['orders_list_success']
        orders = response.json()
        assert isinstance(orders, list), "Ответ должен быть списком"

        # Если есть заказы, проверяем структуру
        if orders:
            first_order = orders[0]
            expected_fields = ["id", "courierId", "track", "color", "createdAt"]
            for field in expected_fields:
                assert field in first_order, f"Поле '{field}' отсутствует в заказе"

            # Проверяем типы данных
            assert isinstance(first_order["id"], int)
            assert isinstance(first_order["courierId"], int)
            assert isinstance(first_order["track"], int)
            if first_order["color"]:  # Если цвет указан
                assert isinstance(first_order["color"], list)
                for color in first_order["color"]:
                    assert color in ["BLACK", "GREY"]
            assert isinstance(first_order["createdAt"], str)