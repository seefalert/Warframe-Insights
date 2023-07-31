import os
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import base64
from urllib.parse import urlparse, urljoin
import re
from PIL import Image



def get_mod_names_from_file(mods_file_path):
    """
    Получает список названий модов из указанного файла.

    Параметры:
        mods_file_path (str): Путь к файлу с названиями модов.

    Возвращает:
        list: Список названий модов.

    Пример использования:
        mods_file_path = "other_from_game/mods_ru"
        mod_names = get_mod_names_from_file(mods_file_path)
        print(mod_names)
    """
    with open(mods_file_path, 'r', encoding='utf-8') as file:
        mod_names = [line.strip() for line in file]

    return mod_names


def get_image_url(mod_name):
    """
    Получает URL изображения для указанного мода с Warframe Wiki.

    Параметры:
        mod_name (str): Название мода.

    Возвращает:
        str: URL изображения мода.
    """
    base_url = "https://warframe.fandom.com/ru/wiki/"
    mod_name_with_underscores = mod_name.replace(" ", "_")
    full_url = base_url + mod_name_with_underscores
    response = requests.get(full_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        image_tag = soup.select_one('a.image img')
        if image_tag:
            image_url = image_tag['src']
            return image_url

    print(f'Не удалось скачать {mod_name}')
    return None


def download_images(mod_names, output_dir):
    """
    Загружает изображения для каждого мода и сохраняет их в указанную папку.

    Параметры:
        mod_names (list): Список названий модов.
        output_dir (str): Путь к папке, в которую будут сохранены изображения.

    Возвращает:
        list: Список пар (название мода, путь к сохраненному изображению).
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    mod_image_list = []
    skipped_mods = []  # Список для хранения пропущенных модов
    for mod_name in tqdm(mod_names, desc="Загрузка изображений"):
        image_url = get_image_url(mod_name)
        if image_url:
            image_path = os.path.join(output_dir, f"{mod_name}.jpg")
            if not os.path.exists(image_path):
                if image_url.startswith('data:image'):
                    # Обрабатываем Base64-кодированное изображение
                    try:
                        # Извлекаем Base64-кодированную строку из URL
                        image_data = image_url.split(",")[1]

                        # Декодируем Base64-строку и создаем изображение
                        image = Image.open(BytesIO(base64.b64decode(image_data)))

                        # Конвертируем изображение в режим RGB
                        if image.mode == 'RGBA':
                            image = image.convert('RGB')

                        image.save(image_path)
                    except Exception as e:
                        print(f"Пропущена загрузка изображения для мода '{mod_name}'. Ошибка: {e}")
                        skipped_mods.append(mod_name)  # Добавляем название мода в список пропущенных
                        continue
                else:
                    # Обрабатываем обычную ссылку на удаленный ресурс
                    base_url = "https://warframe.fandom.com/ru/wiki/"
                    image_url = urljoin(base_url, image_url)
                    try:
                        # Загружаем изображение с помощью библиотеки Pillow
                        image = Image.open(requests.get(image_url, stream=True).raw)

                        # Конвертируем изображение в режим RGB
                        if image.mode == 'RGBA':
                            image = image.convert('RGB')

                        image.save(image_path)
                    except Exception as e:
                        print(f"Пропущена загрузка изображения для мода '{mod_name}'. Ошибка: {e}")
                        skipped_mods.append(mod_name)  # Добавляем название мода в список пропущенных
                        continue
            mod_image_list.append((mod_name, image_path))

    # Выводим список пропущенных модов
    if skipped_mods:
        print("\nПропущены изображения для следующих модов:")
        for mod in skipped_mods:
            print(mod)

    return mod_image_list


def main():
    mods_file_path = "other_from_game/mods_ru"
    mod_names = get_mod_names_from_file(mods_file_path)

    output_dir = "mod_images"
    mod_image_list = download_images(mod_names, output_dir)

    with open("mod_images_list.txt", "w", encoding="utf-8") as file:
        for mod_name, image_path in mod_image_list:
            file.write(f"{image_path}\t{mod_name}\n")


if __name__ == "__main__":
    main()


