import allure
import pytest
import requests

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"

@allure.feature("Создание курьера")
class TestCourierCreation:

    @allure.story("Успешное создание курьера")
    def test_create_courier_success(self, courier_data):
        courier = courier_data()
        assert courier is not None
        assert courier["response"].status_code == 201
        assert courier["response"].json() == {"ok": True}

    @allure.story("Нельзя создать дублирующего курьера")
    def test_cannot_create_duplicate_courier(self, courier_data):
        # Создаём первого курьера
        first_courier = courier_data()
        assert first_courier is not None

        # Пытаемся создать второго с теми же данными
        payload = {
            "login": first_courier["login"],
            "password": first_courier["password"],
            "firstName": first_courier["first_name"]
        }
        response = requests.post(f"{BASE_URL}/courier", data=payload)
        assert response.status_code == 409

    @pytest.mark.parametrize("missing_field", ["login", "password", "firstName"])
    @allure.story("Проверка обязательных полей")
    def test_missing_required_fields(self, missing_field):
        login, password, first_name = "testlogin", "testpass", "testname"
        payload = {"login": login, "password": password, "firstName": first_name}
        del payload[missing_field]

        response = requests.post(f"{BASE_URL}/courier", data=payload)
        assert response.status_code in [400, 404]
        assert "message" in response.json()