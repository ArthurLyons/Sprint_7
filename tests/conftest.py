import pytest
from config.config import BASE_URL, EXPECTED_STATUS_CODES
from helpers.api_helpers import post_request, generate_random_string


@pytest.fixture
def courier_data():
    """Фикстура: создаёт курьера и очищает после теста"""
    created_couriers = []

    def _create_courier():
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        response = post_request(f"{BASE_URL}/courier", payload)

        if response.status_code == EXPECTED_STATUS_CODES['create_courier_success']:
            courier = {
                "login": login,
                "password": password,
                "first_name": first_name,
                "response": response
            }
            created_couriers.append(courier)
            return courier
        return None

    yield _create_courier

    # Очистка: попытка удалить курьера (если API поддержит в будущем)
    for courier in created_couriers:
        login_payload = {
            "login": courier["login"],
            "password": courier["password"]
        }
        login_response = post_request(f"{BASE_URL}/login", login_payload)
        if login_response.status_code == EXPECTED_STATUS_CODES['login_success']:
            courier_id = login_response.json().get("id")
            if courier_id:
                # Пока API не поддерживает удаление, оставляем заглушку
                pass


@pytest.fixture
def created_courier_id(courier_data):
    """Фикстура: создаёт курьера и возвращает его ID"""
    courier = courier_data()
    assert courier is not None

    login_payload = {
        "login": courier["login"],
        "password": courier["password"]
    }
    login_response = post_request(f"{BASE_URL}/login", login_payload)
    assert login_response.status_code == EXPECTED_STATUS_CODES['login_success']
    return login_response.json()["id"]