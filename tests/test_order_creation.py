import allure
import pytest
import requests

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"

@allure.feature("Создание заказа")
class TestOrderCreation:

    @pytest.fixture
    def courier_id(self, courier_data):
        courier = courier_data()
        assert courier is not None

        payload = {
            "login": courier["login"],
            "password": courier["password"]
        }
        response = requests.post(f"{BASE_URL}/login", data=payload)
        return response.json()["id"]

    @pytest.mark.parametrize("color", [["BLACK"], ["GREY"], ["BLACK", "GREY"], []])
    @allure.story("Создание заказа с разными вариантами цвета")
    def test_order_creation_with_different_colors(self, courier_id, color):
        payload = {"courierId": courier_id}
        if color:
            payload["color"] = color

        response = requests.post(f"{BASE_URL}/orders", data=payload)
        assert response.status_code == 201
        assert "track" in response.json()
        assert isinstance(response.json()["track"], int)