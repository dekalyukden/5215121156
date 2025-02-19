import tkinter as tk
from tkinter import ttk
import cv2
import keyboard
import numpy as np
import pyautogui
from utils.key_handler import choose_key, load_key
from utils.image_processor import select_region
from utils.logger import log_message

def center_window(root, width=300, height=300):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    root.geometry(f"{width}x{height}+{x}+{y}")

def run_app():
    global selected_key, x_start, y_start, x_end, y_end, cropping, image, image_copy

    log_message("Захоплення зображення з екрану")
    image = np.array(pyautogui.screenshot())
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # Конвертує зображення з формату RGB у формат BGR
    image_copy = image.copy()  # Створює копію зображення

    x_start, y_start, x_end, y_end = None, None, None, None
    cropping = False

    # Створення вікна tkinter
    root = tk.Tk()
    root.title("Програма виділення області")  # Встановлює назву вікна
    center_window(root)  # Відкриває вікно по центру екрану

    selected_key = load_key()

    choose_key_button = ttk.Button(root, text="Призначити кнопку", command=lambda: choose_key(key_label))  # Зміна тексту кнопки
    choose_key_button.pack(pady=10)

    key_label = ttk.Label(root, text=f"Обрана клавіша: {selected_key if selected_key else 'Не обрано'}")
    key_label.pack()

    def start_selection():
        global selected_key, x_start, y_start, x_end, y_end, cropping, image, image_copy

        if selected_key is None:
            print("Помилка: Не обрано клавішу для виділення.")
            return

        cv2.namedWindow("Screen")
        cv2.setMouseCallback("Screen", select_region)
        log_message("Створено вікно для відображення зображення")

        while True:
            cv2.imshow("Screen", image_copy)
            key = keyboard.read_event()
            if key and key.event_type == keyboard.KEY_DOWN and key.name == selected_key:
                cv2.destroyAllWindows()
                break
            if key and key.event_type == keyboard.KEY_DOWN and key.name == 'q':
                cv2.destroyAllWindows()
                log_message("Вікно закрито")
                if all(coord is not None for coord in [x_start, y_start, x_end, y_end]):
                    print("Координати виділеної області:")
                    print(f"x_start: {x_start}, y_start: {y_start}")
                    print(f"x_end: {x_end}, y_end: {y_end}")
                    log_message(f"Координати: ({x_start}, {y_start}), ({x_end}, {y_end})")
                log_message("Завершення роботи програми")
                return

    start_button = ttk.Button(root, text="Запустити виділення", command=start_selection)
    start_button.pack(pady=10)

    root.mainloop()
