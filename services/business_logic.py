def analyze_orders(orders, status=None, order_type=None, current_year_only=True):
    """
    analyze_orders
    Анализирует список заказов и вычисляет некоторые статистические данные.

    Параметры:
        orders (list): Список словарей с информацией о заказах.
        status (str, optional): Фильтр по статусу пользователя заказов. По умолчанию None.
                                Возможные значения: 'ingame', 'online', 'offline'.
        order_type (str, optional): Фильтр по типу заказа (покупка/продажа). По умолчанию None.
                                    Возможные значения: 'sell', 'buy'.
        current_year_only (bool, optional): Флаг, определяющий, нужно ли учитывать заказы только из текущего года.
                                            По умолчанию True.

    Возвращает:
        dict: Словарь с некоторыми статистическими данными о заказах.
              Возможные ключи:
              - "min_platinum": Самое дешёвое значение platinum.
              - "max_platinum": Самое дорогое значение platinum.
              - "average_platinum": Средняя стоимость platinum.

    Пример использования:
        orders_list = get_item_orders("mirage_prime_systems")
        results = analyze_orders(orders_list, status='online', order_type='sell', current_year_only=True)
        if results:
            print(f"Самое дешёвое значение platinum: {results['min_platinum']}")
            print(f"Самое дорогое значение platinum: {results['max_platinum']}")
            print(f"Средняя стоимость platinum: {results['average_platinum']}")
    """
    # Внутренняя функция для фильтрации заказов
    def filter_orders(order):
        if status and order['user']['status'] != status:
            return False
        if order_type and order['order_type'] != order_type:
            return False
        if current_year_only and int(order['last_update'][:4]) != datetime.now().year:
            return False
        return True

    # Фильтруем заказы
    selected_orders = filter(filter_orders, orders)

    # Если нет выбранных заказов, выводим сообщение и возвращаем None
    if not selected_orders:
        print(f"Нет заказов с параметрами: status='{status}', order_type='{order_type}', current_year_only={current_year_only}")
        return None

    # Вычисляем суммарное количество единиц (quantity) и суммарное количество платины
    total_quantity = sum(order['quantity'] for order in selected_orders)
    total_platinum = sum(order['platinum'] * order['quantity'] for order in selected_orders)

    # Вычисляем среднюю стоимость platinum
    average_platinum = total_platinum / total_quantity

    # Получение самого дешевого и самого дорогое значения platinum
    min_platinum = min(order['platinum'] for order in selected_orders)
    max_platinum = max(order['platinum'] for order in selected_orders)

    # Возвращаем результаты в виде словаря
    result = {
        "min_platinum": min_platinum,
        "max_platinum": max_platinum,
        "average_platinum": average_platinum
    }

    return result
