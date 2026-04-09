import allure
import pytest
from config.config import BASE_URL, EXPECTED_STATUS_CODES, EXPECTED_ERROR_MESSAGES
from helpers.api_helpers import post_request, generate_random_string


@allure.feature("Создание курьера")
class TestCourierCreation:

    @allure.title("Успешное создание курьера")
    def test_create_courier_success(self, courier_data):
        courier = courier_data()
        assert courier is not None
        assert courier["response"].status_code == EXPECTED_STATUS_CODES['create_courier_success']
        assert courier["response"].json() == {"ok": True}

    @allure.title("Попытка создания курьера с существующим логином")
    def test_cannot_create_duplicate_courier(self, courier_data):
        first_courier = courier_data()
        assert first_courier is not None

        payload = {
            "login": first_courier["login"],
            "password": "new_pass",
            "firstName": "Another"
        }
        response = post_request(f"{BASE_URL}/courier", payload)
        assert response.status_code == EXPECTED_STATUS_CODES['create_courier_duplicate']
        assert response.json()["message"] == EXPECTED_ERROR_MESSAGES['duplicate_courier']

    @pytest.mark.parametrize("missing_field", ["login", "password", "firstName"])
    @allure.title("Ошибка при отсутствии обязательного поля: {missing_field}")
    def test_missing_required_fields(self, missing_field):
        login, password, first_name = "testlogin", "testpass", "testname"
        payload = {"login": login, "password": password, "firstName": first_name}
        del payload[missing_field]

        response = post_request(f"{BASE_URL}/courier", payload)
        assert response.status_code == EXPECTED_STATUS_CODES['create_courier_missing_field']
        assert response.json()["message"] == EXPECTED_ERROR_MESSAGES['missing_required_field']