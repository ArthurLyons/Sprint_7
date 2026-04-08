import allure
import pytest
from config import BASE_URL, EXPECTED_STATUS_CODES, EXPECTED_ERROR_MESSAGES
from helpers.api_helpers import post_request

@allure.feature("Создание курьера")
class TestCourierCreation:

    @allure.title("Успешное создание курьера")
    @allure.story("Регистрация нового курьера с корректными данными")
    def test_create_courier_success(self, courier_data):
        courier = courier_data()
        assert courier is not None
        assert courier["response"].status_code == EXPECTED_STATUS_CODES['create_courier_success']
        response_json = courier["response"].json()
        assert response_json == {"ok": True}

    @allure.title("Попытка создания дублирующего курьера")
    @allure.story("Проверка запрета регистрации курьера с существующим логином")
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
        response = post_request(f"{BASE_URL}/courier", payload)
        assert response.status_code == EXPECTED_STATUS_CODES['create_courier_duplicate']
        response_json = response.json()
        assert "message" in response_json
        assert response_json["message"] == EXPECTED_ERROR_MESSAGES['duplicate_courier']

    @pytest.mark.parametrize("missing_field", ["login", "password", "firstName"])
    @allure.title("Проверка отсутствия обязательного поля: {missing_field}")
    @allure.story("Валидация обязательных полей при создании курьера")
    def test_missing_required_fields(self, missing_field):
        login, password, first_name = "testlogin", "testpass", "testname"
        payload = {"login": login, "password": password, "firstName": first_name}
        del payload[missing_field]

        response = post_request(f"{BASE_URL}/courier", payload)
        assert response.status_code == EXPECTED_STATUS_CODES['create_courier_missing_field']
        response_json = response.json()
        assert "message" in response_json
        assert response_json["message"] == EXPECTED_ERROR_MESSAGES['missing_required_field']