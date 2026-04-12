BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"

EXPECTED_STATUS_CODES = {
    'create_courier_success': 201,
    'create_courier_duplicate': 409,
    'create_courier_missing_field': 400,
    'login_success': 200,
    'login_invalid_credentials': 404,
    'order_creation_success': 201,
    'orders_list_success': 200
}

EXPECTED_ERROR_MESSAGES = {
    'missing_required_field': 'Недостаточно данных для создания курьера',
    'duplicate_courier': 'Этот логин уже используется. Попробуйте другой.',
    'invalid_credentials': 'Учётные данные не верны'
}