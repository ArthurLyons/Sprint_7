import pytest
import requests
import random
import string

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"

def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


@pytest.fixture
def courier_data():
    """Фикстура для создания и удаления курьера"""
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

        response = requests.post(f"{BASE_URL}/courier", data=payload)
        if response.status_code == 201:
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

    # Очистка созданных курьеров
    for courier in created_couriers:
        # Получаем ID курьера через логин/пароль
        login_payload = {
            "login": courier["login"],
            "password": courier["password"]
        }
        login_response = requests.post(f"{BASE_URL}/login", data=login_payload)
        if login_response.status_code == 200:
            courier_id = login_response.json().get("id")
            if courier_id:
                # Здесь можно добавить запрос на удаление курьера, если API поддерживает
                pass