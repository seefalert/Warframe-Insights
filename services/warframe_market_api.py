"""
Модуль для работы с API Warframe.market.

Функции:
- get_items_list: Получает список предметов из Warframe.market API.
- login: Аутентифицирует пользователя на Warframe.market API.
- get_item_orders: Получает список заказов для указанного предмета с Warframe.market API.
"""


from config_data.config import load_config

import requests


def get_items_list(cookie_auth, language='ru', platform='pc'):
    """
    Получает список предметов с Warframe.market API и возвращает его.

    Параметры:
        cookie_auth (str): Значение Cookie_Auth для аутентификации запросов.
        language (str, optional): Язык запроса. По умолчанию 'ru'.
        platform (str, optional): Платформа для фильтрации предметов. По умолчанию 'pc'.

    Возвращает:
        list: Список словарей с информацией о предметах.

    Пример использования:
        cookie_auth = 'seefalert'
        language = 'ru'
        platform = 'pc'
        items_list = get_items_list(cookie_auth, language, platform)
        if items_list:
            for item in items_list:
                print(item['item_name'])
    """
    headers = {
        'Cookie_Auth': cookie_auth,
        'Language': language,
        'Platform': platform  # Можно указать другую доступную платформу: xbox, ps4, switch
    }
    url = 'https://api.warframe.market/v1'
    endpoint = '/items'
    response = requests.get(url + endpoint, headers=headers)

    if response.status_code == 200:
        data = response.json()
        items_list = data['payload']['items']

        # Сортируем список предметов по алфавиту по полю 'item_name'
        items_list.sort(key=lambda item: item['item_name'])
        return items_list
    else:
        return None


def login(email, password):
    """
    Выполняет вход на Warframe.market API с использованием email и пароля.

    Параметры:
        email (str): Email пользователя для входа.
        password (str): Пароль пользователя для входа.

    Возвращает:
        dict: Словарь с данными о пользователе и токеном.

    Пример использования:
        email = 'example@example.com'
        password = 'mypassword'
        user_data = login(email, password)
        if user_data:
            print("Успешный вход!")
            print("Токен:", user_data['token'])
            print("ID пользователя:", user_data['user']['id'])
        else:
            print("Ошибка входа. Проверьте email и пароль.")
    """
    url = 'https://api.warframe.market/v1/auth/signin'
    jwt_header = 'JWT seefalert'

    headers = {
        'Authorization': jwt_header
    }
    payload = {
        'email': email,
        'password': password
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()
    else:
        return None


def get_item_orders(url, url_name, cookie_auth, language='ru', platform='pc'):
    """
    Получает список заказов для указанного предмета с Warframe.market API.

    Параметры:
        url (str): Базовый URL для запросов к Warframe.market API.
        url_name (str): Уникальное имя предмета в формате URL.
        cookie_auth (str): Значение Cookie_Auth для аутентификации запросов.
        language (str, optional): Язык запроса. По умолчанию 'ru'.
        platform (str, optional): Платформа для фильтрации заказов. По умолчанию 'pc'.

    Возвращает:
        list: Список словарей с данными о заказах для указанного предмета.

    Пример использования:
        base_url = 'https://api.warframe.market/v1'
        url_name = 'mirage_prime_systems'
        cookie_auth = 'seefalert'
        language = 'en'
        platform = 'pc'
        orders_list = get_item_orders(base_url, url_name, cookie_auth, language, platform)
        if orders_list:
            print(f"Загружено {len(orders_list)} заказов.")
        else:
            print("Ошибка загрузки заказов. Проверьте параметры запроса.")
    """
    endpoint = f'/items/{url_name}/orders'
    headers = {
        'Cookie_Auth': cookie_auth,
        'Language': language,
        'Platform': platform
    }

    response = requests.get(url + endpoint, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data['payload']['orders']
    else:
        return None


if __name__ == "__main__":
    config = load_config()

    # URL API Warframe.market
    url = 'https://api.warframe.market/v1'

    cookie_auth = 'seefalert'
    headers = {
        'Cookie_Auth': 'seefalert',
        'Language': 'ru',
        'Platform': 'pc'  # Можно указать другую доступную платформу: xbox, ps4, switch
    }

    # Пример использования функции get_items_list
    items_list = get_items_list()
    if items_list:
        print(f"Загружено {len(items_list)} предметов.")
    else:
        print("Ошибка загрузки списка предметов. Проверьте параметры запроса.")

    # Пример использования функции login
    email = config.auth.email
    password = config.auth.password
    login_response = login(email, password)
    if login_response:
        print("Успешная аутентификация. Полученные данные:")
        print(login_response)
    else:
        print("Ошибка аутентификации. Проверьте правильность введенных данных.")

    # Пример использования функции get_item_orders
    # URL-имя предмета для анализа
    item_url_name = 'mirage_prime_systems'
    orders_list = get_item_orders(url, item_url_name, cookie_auth, language='ru', platform='pc')
    if orders_list:
        print(f"Загружено {len(orders_list)} заказов для предмета {item_url_name}.")
    else:
        print(f"Ошибка загрузки заказов для предмета {item_url_name}. Проверьте параметры запроса.")
