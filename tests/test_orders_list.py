import allure
import requests

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"


@allure.feature("Список заказов")
class TestOrdersList:

    @allure.story("Получение списка заказов")
    def test_get_orders_list(self):
        response = requests.get(f"{BASE_URL}/orders")
        assert response.status_code == 200
        orders = response.json()
        assert isinstance(orders, list), "Ответ должен быть списком"

        # Если есть заказы, проверяем структуру
        if orders:
            first_order = orders[0]
            expected_fields = ["id", "courierId", "track", "color", "createdAt"]
            for field in expected_fields:
                assert field in first_order, f"Поле '{field}' отсутствует в заказе"

    @allure.story("Проверка структуры отдельного заказа")
    def test_order_structure_in_list(self):
        response = requests.get(f"{BASE_URL}/orders")
        assert response.status_code == 200
        orders = response.json()

        for order in orders:
            # Проверяем типы данных
            assert isinstance(order["id"], int)
            assert isinstance(order["courierId"], int)
            assert isinstance(order["track"], int)
            if order["color"]:  # Если цвет указан
                assert isinstance(order["color"], list)
                for color in order["color"]:
                    assert color in ["BLACK", "GREY"]
            assert "createdAt" in order