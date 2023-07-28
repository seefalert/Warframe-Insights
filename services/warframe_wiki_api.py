"""
Модуль warframe_wiki_api предоставляет функции для работы с веб-страницами Warframe Wiki,
а также для нахождения общих элементов между различными списками.

Включает функции:
- get_mod_names(url): Получает список названий модов с указанной веб-страницы.
- save_sorted_unique_elements(output_file_path, elements_list): Сохраняет отсортированный список
                                                                уникальных элементов в файл.
- find_common_elements(mod_names, items_file_path): Находит общие элементы между списком модов
                                                    и списком элементов из файла.
"""


import requests
from bs4 import BeautifulSoup


def get_mod_names(url):
    """
    Получает список названий модов с указанной веб-страницы.

    Параметры:
        url (str): URL веб-страницы с модами.

    Возвращает:
        list: Список названий модов.

    Пример использования:
        url_ru = "https://warframe.fandom.com/ru/wiki/Категория:Моды"
        mod_names_ru = get_mod_names(url_ru)
        print(mod_names_ru)
    """
    mod_names = []

    while url:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        mod_elements = soup.select('.category-page__member-link')
        mod_names.extend(mod.text for mod in mod_elements)

        next_button = soup.find('a', {'class': 'category-page__pagination-next'})
        if not next_button:
            break

        url = next_button['href']

    return mod_names


def save_sorted_unique_elements(output_file_path, elements_list):
    """
    Сохраняет отсортированный список уникальных элементов в файл.

    Параметры:
        output_file_path (str): Путь к файлу, в который будут сохранены элементы.
        elements_list (list): Список элементов для сохранения.

    Возвращает:
        None
    """
    # Преобразуем список во множество, чтобы удалить дубликаты
    unique_elements = set(elements_list)

    # Преобразуем результат обратно в список и сортируем его
    result_list = sorted(list(unique_elements))

    # Сохраняем результат в новый файл
    with open(output_file_path, 'w', encoding='utf-8') as file:
        for item in result_list:
            file.write(item + '\n')


def find_common_elements(mod_names, items_file_path):
    """
    Находит общие элементы между списком модов и списком элементов из файла.

    Параметры:
        mod_names (list): Список модов.
        items_file_path (str): Путь к файлу, содержащему список элементов.

    Возвращает:
        list: Список общих элементов.
    """
    # Считываем данные из файла items_file_path
    with open(items_file_path, 'r', encoding='utf-8') as file:
        list1 = [line.strip() for line in file]

    # Преобразуем списки во множества
    set1 = set(list1)
    set2 = set(mod_names)

    # Находим пересечение множеств (элементы, которые есть и в первом, и во втором списке)
    common_elements = set1.intersection(set2)

    # Преобразуем результат обратно в список и сортируем его
    result_list = sorted(list(common_elements))

    return result_list


if __name__ == "__main__":
    # Пример использования функций
    pass
