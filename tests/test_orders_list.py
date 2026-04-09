import allure
from config.config import BASE_URL, EXPECTED_STATUS_CODES
from helpers.api_helpers import get_request


@allure.feature("Список заказов")
class TestOrdersList:

    @allure.title("Получение списка заказов")
    def test_get_orders_list(self):
        response = get_request(f"{BASE_URL}/orders")
        assert response.status_code == EXPECTED_STATUS_CODES['orders_list_success']
        orders = response.json()
        assert isinstance(orders, list)