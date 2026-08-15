"""
API Request Example – Pet Project

Проект: Web Application (учебный pet-проект)
Модуль: REST API (авторизация, пользователи, заказы)
Дата: 13.08.2026
Автор: Shar Lodka
Инструменты: Python, requests, json

Этот скрипт демонстрирует базовую работу с REST API:
- авторизация (получение токена);
- получение данных пользователя;
- создание заказа.

Перед запуском установите зависимости:
    pip install requests
"""

import requests

BASE_URL = "https://example-app.com/api"


def login(email: str, password: str) -> dict:
    """
    Авторизация пользователя.

    Возвращает JSON-ответ с токеном и данными пользователя.
    """
    url = f"{BASE_URL}/auth/login"
    payload = {
        "email": email,
        "password": password,
    }
    response = requests.post(url, json=payload)

    # Простая проверка статус-кода
    if response.status_code != 200:
        raise RuntimeError(
            f"Login failed with status {response.status_code}: {response.text}"
        )

    return response.json()


def get_user(user_id: int, token: str) -> dict:
    """
    Получение данных пользователя по ID.

    Требует авторизации через Bearer-токен.
    """
    url = f"{BASE_URL}/users/{user_id}"
    headers = {
        "Authorization": f"Bearer {token}",
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise RuntimeError(
            f"Get user failed with status {response.status_code}: {response.text}"
        )

    return response.json()


def create_order(token: str, items: list, address: str) -> dict:
    """
    Создание нового заказа.

    items – список вида:
        [
            {"product_id": 10, "quantity": 2},
            {"product_id": 5, "quantity": 1},
        ]
    """
    url = f"{BASE_URL}/orders"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    payload = {
        "items": items,
        "address": address,
    }
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code not in (200, 201):
        raise RuntimeError(
            f"Create order failed with status {response.status_code}: {response.text}"
        )

    return response.json()


def main():
    # Данные для авторизации 
    email = "user@example.com"
    password = "Test200!"

    # 1. Авторизация
    login_response = login(email, password)
    token = login_response["token"]
    user_id = login_response["user_id"]
    print("Login successful:")
    print(f"  user_id: {user_id}")
    print(f"  token: {token[:20]}...")  

    # 2. Получение данных пользователя
    user_data = get_user(user_id, token)
    print("\nUser data:")
    print(f"  id: {user_data.get('id')}")
    print(f"  name: {user_data.get('name')}")
    print(f"  email: {user_data.get('email')}")

    # 3. Создание заказа
    items = [
        {"product_id": 10, "quantity": 2},
        {"product_id": 5, "quantity": 1},
    ]
    address = "Archacity, st. Example, 1"

    order_response = create_order(token, items, address)
    print("\nOrder created:")
    print(f"  order_id: {order_response.get('order_id')}")
    print(f"  status: {order_response.get('status')}")
    print(f"  items: {order_response.get('items')}")
    print(f"  address: {order_response.get('address')}")


if __name__ == "__main__":
    main()
