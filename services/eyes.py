from time import sleep

import cv2
import pytesseract
import pygetwindow as gw
import pyautogui
import numpy as np
from PIL import Image

def recognize_text_from_window(window_title, lang='eng'):
    try:
        window = gw.getWindowsWithTitle(window_title)[0]
        x, y, width, height = window.left, window.top, window.width, window.height
        screenshot = pyautogui.screenshot(region=(x, y, width, height))
        image_np = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray, lang=lang)
        return text
    except IndexError:
        print(f"Окно с заголовком '{window_title}' не найдено.")
        return None


def main():
    # Загрузка модели Tesseract OCR
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

    while True:
        # Распознавание текста на английском языке
        window_title = "Завершение_Начатого_вики.png"  # Замените на заголовок окна, которое нужно сканировать
        text = recognize_text_from_window(window_title, lang='eng')

        # Вывод распознанного текста в консоль
        if text:
            print(f"Распознанный текст (английский): {text}")

        # Распознавание текста на русском языке
        window_title_ru = "Завершение_Начатого_вики.png"  # Замените на заголовок окна с русским текстом
        text_ru = recognize_text_from_window(window_title_ru, lang='rus')

        # Вывод распознанного текста на русском в консоль
        if text_ru:
            print(f"Распознанный текст (русский): {text_ru}")
        print('Ищу текст...')
        sleep(5)

if __name__ == "__main__":
    main()
