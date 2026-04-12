import allure
import requests
import random
import string


@allure.step("POST запрос к {endpoint}")
def post_request(endpoint, payload=None):
    response = requests.post(endpoint, data=payload, timeout=10)
    allure.attach(
        body=str(payload),
        name="Request payload",
        attachment_type=allure.attachment_type.JSON
    )
    allure.attach(
        body=response.text,
        name="Response body",
        attachment_type=allure.attachment_type.JSON
    )
    return response


@allure.step("GET запрос к {endpoint}")
def get_request(endpoint):
    response = requests.get(endpoint, timeout=10)
    allure.attach(
        body="",
        name="Request payload",
        attachment_type=allure.attachment_type.JSON
    )
    allure.attach(
        body=response.text,
        name="Response body",
        attachment_type=allure.attachment_type.JSON
    )
    return response


def generate_random_string(length):
    """Вынос примитивной логики в helpers — разрешённо"""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))