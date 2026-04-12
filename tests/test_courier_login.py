import allure
import pytest
from config.config import BASE_URL, EXPECTED_STATUS_CODES, EXPECTED_ERROR_MESSAGES
from helpers.api_helpers import post_request


@allure.feature("Авторизация курьера")
class TestCourierLogin:

    @allure.title("Успешная авторизация курьера")
    def test_courier_can_login(self, courier_data):
        courier = courier_data()
        assert courier is not None

        payload = {
            "login": courier["login"],
            "password": courier["password"]
        }
        response = post_request(f"{BASE_URL}/login", payload)
        assert response.status_code == EXPECTED_STATUS_CODES['login_success']
        assert "id" in response.json()
        assert isinstance(response.json()["id"], int)

    @pytest.mark.parametrize("field_to_remove", ["login", "password"])
    @allure.title("Ошибка при отсутствии поля: {field_to_remove}")
    def test_login_requires_all_fields(self, field_to_remove):
        payload = {"login": "test", "password": "pass"}
        del payload[field_to_remove]
        response = post_request(f"{BASE_URL}/login", payload)
        assert response.status_code == EXPECTED_STATUS_CODES['login_invalid_credentials']
        assert response.json()["message"] == EXPECTED_ERROR_MESSAGES['invalid_credentials']

    @allure.title("Ошибка при неверном пароле")
    def test_login_with_wrong_password(self, courier_data):
        courier = courier_data()
        assert courier is not None

        payload = {
            "login": courier["login"],
            "password": "wrong_password"
        }
        response = post_request(f"{BASE_URL}/login", payload)
        assert response.status_code == EXPECTED_STATUS_CODES['login_invalid_credentials']
        assert response.json()["message"] == EXPECTED_ERROR_MESSAGES['invalid_credentials']

    @allure.title("Ошибка при авторизации несуществующего курьера")
    def test_nonexistent_courier_cannot_login(self):
        payload = {
            "login": "nonexistent_login_123",
            "password": "nonexistent_pass"
        }
        response = post_request(f"{BASE_URL}/login", payload)
        assert response.status_code == EXPECTED_STATUS_CODES['login_invalid_credentials']
        assert response.json()["message"] == EXPECTED_ERROR_MESSAGES['invalid_credentials']