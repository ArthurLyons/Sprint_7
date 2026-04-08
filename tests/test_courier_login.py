import allure
import pytest
from config import BASE_URL, EXPECTED_STATUS_CODES, EXPECTED_ERROR_MESSAGES
from helpers.api_helpers import post_request


@allure.feature("Авторизация курьера")
class TestCourierLogin:

    @allure.title("Успешная авторизация существующего курьера")
    @allure.story("Вход в систему с корректными учётными данными")
    def test_courier_can_login(self, courier_data):
        courier = courier_data()
        assert courier is not None

        payload = {
            "login": courier["login"],
            "password": courier["password"]
        }
        response = post_request(f"{BASE_URL}/login", payload)
        assert response.status_code == EXPECTED_STATUS_CODES['login_success']
        response_json = response.json()
        assert "id" in response_json
        assert isinstance(response_json["id"], int)

    @pytest.mark.parametrize("field_to_remove", ["login", "password"])
    @allure.title("Проверка отсутствия поля авторизации: {field_to_remove}")
    @allure.story("Валидация обязательных полей для авторизации")
    def test_login_requires_all_fields(self, field_to_remove):
        payload = {"login": "test", "password": "pass"}
        del payload[field_to_remove]
        response = post_request(f"{BASE_URL}/login", payload)
        assert response.status_code in [400, 404]
        response_json = response.json()
        assert "message" in response_json


    @allure.title("Ошибка при авторизации с неверными учётными данными")
    @allure.story("Проверка ошибки при вводе неправильного пароля")
    def test_incorrect_credentials_return_error(self, courier_data):
        courier = courier_data()
        assert courier is not None

        payload = {
            "login": courier["login"],
            "password": "wrong_password"
        }
        response = post_request(f"{BASE_URL}/login", payload)
        assert response.status_code == EXPECTED_STATUS_CODES['login_invalid_credentials']
        response_json = response.json()
        assert "message" in response_json
        assert response_json["message"] == EXPECTED_ERROR_MESSAGES['invalid_credentials']

    @allure.title("Ошибка при авторизации несуществующего курьера")
    @allure.story("Проверка ошибки при попытке входа несуществующего курьера")
    def test_nonexistent_courier_cannot_login(self):
        payload = {
            "login": "nonexistent_login",
            "password": "nonexistent_password"
        }
        response = post_request(f"{BASE_URL}/login", payload)
        assert response.status_code == EXPECTED_STATUS_CODES['login_invalid_credentials']
        response_json = response.json()
        assert "message" in response_json
        assert response_json["message"] == EXPECTED_ERROR_MESSAGES['invalid_credentials']