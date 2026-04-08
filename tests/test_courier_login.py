import allure
import requests
import pytest

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"

@allure.feature("Авторизация курьера")
class TestCourierLogin:

    @allure.story("Успешная авторизация")
    def test_courier_can_login(self, courier_data):
        courier = courier_data()
        assert courier is not None

        payload = {
            "login": courier["login"],
            "password": courier["password"]
        }
        response = requests.post(f"{BASE_URL}/login", data=payload)
        assert response.status_code == 200
        assert "id" in response.json()

    @pytest.mark.parametrize("field_to_remove", ["login", "password"])
    @allure.story("Проверка обязательных полей для авторизации")
    def test_login_requires_all_fields(self, field_to_remove):
        payload = {"login": "test", "password": "pass"}
        del payload[field_to_remove]
        response = requests.post(f"{BASE_URL}/login", data=payload)
        assert response.status_code in [400, 404]

    @allure.story("Ошибка при неверных учётных данных")
    def test_incorrect_credentials_return_error(self, courier_data):
        courier = courier_data()
        assert courier is not None

        payload = {
            "login": courier["login"],
            "password": "wrong_password"
        }
        response = requests.post(f"{BASE_URL}/login", data=payload)
        assert response.status_code == 404