import os

from config_data.config import load_config
from services.warframe_wiki_api import get_mod_names, save_sorted_unique_elements, find_common_elements
from services.warframe_market_api import get_items_list

# Загружаем конфиг в переменную config
config = load_config()


def update_all_files():
    """
    Актуализирует все файлы в папке "other_from_game" с использованием функций из модуля warframe_wiki_api.
    """
    base_dir = "other_from_game"
    items_en_file = os.path.join(base_dir, "items_en")
    items_ru_file = os.path.join(base_dir, "items_ru")
    mods_en_file = os.path.join(base_dir, "mods_en")
    mods_ru_file = os.path.join(base_dir, "mods_ru")

    # Получаем списки предметов с API
    cookie_auth = 'seefalert'
    items_list_en = get_items_list(cookie_auth, language='en')
    items_list_ru = get_items_list(cookie_auth, language='ru')

    items_en = [item['item_name'] for item in items_list_en]
    items_ru = [item['item_name'] for item in items_list_ru]

    # Сохраняем отсортированные уникальные названия предметов в файлы
    save_sorted_unique_elements(items_en_file, items_en)
    save_sorted_unique_elements(items_ru_file, items_ru)

    # Получаем список названий модов с различных веб-страниц
    mods_url_en = "https://warframe.fandom.com/wiki/Category:Mods"
    mod_names_en = get_mod_names(mods_url_en)

    mods_url_ru = "https://warframe.fandom.com/ru/wiki/Категория:Моды"
    mod_names_ru = get_mod_names(mods_url_ru)

    # Сохраняем отсортированные уникальные названия модов в файлы
    save_sorted_unique_elements(mods_en_file, mod_names_en)
    save_sorted_unique_elements(mods_ru_file, mod_names_ru)

    # Находим общие элементы между списками модов и списками предметов
    common_elements_en = find_common_elements(mod_names_en, "other_from_game/items_en")
    common_elements_ru = find_common_elements(mod_names_ru, "other_from_game/items_ru")

    # Сохраняем общие элементы в файлы
    save_sorted_unique_elements(mods_en_file, common_elements_en)
    save_sorted_unique_elements(mods_ru_file, common_elements_ru)


if __name__ == "__main__":
    update_all_files()
