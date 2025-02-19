import json
import keyboard
from utils.logger import log_message

# Відповідність українських клавіш до латинських (повна розкладка)
UKR_TO_LAT = {
    "й": "q", "ц": "w", "у": "e", "к": "r", "е": "t", "н": "y", "г": "u", "ш": "i", "щ": "o", "з": "p", "х": "[", "ї": "]",
    "ф": "a", "і": "s", "в": "d", "а": "f", "п": "g", "р": "h", "о": "j", "л": "k", "д": "l", "ж": ";", "є": "'",
    "я": "z", "ч": "x", "с": "c", "м": "v", "и": "b", "т": "n", "ь": "m", "б": ",", "ю": ".", ".": "/",
    "Й": "Q", "Ц": "W", "У": "E", "К": "R", "Е": "T", "Н": "Y", "Г": "U", "Ш": "I", "Щ": "O", "З": "P", "Х": "{", "Ї": "}",
    "Ф": "A", "І": "S", "В": "D", "А": "F", "П": "G", "Р": "H", "О": "J", "Л": "K", "Д": "L", "Ж": ":", "Є": "\"",
    "Я": "Z", "Ч": "X", "С": "C", "М": "V", "И": "B", "Т": "N", "Ь": "M", "Б": "<", "Ю": ">", ",": "<", "?": "?", "№": "#"
}

def save_key(key):
    with open('config.json', 'w') as f:
        json.dump({'selected_key': key}, f)

def load_key():
    try:
        with open('config.json', 'r') as f:
            data = json.load(f)
            return data['selected_key']
    except FileNotFoundError:
        return None

def choose_key(key_label):
    global selected_key
    key_label.config(text="Чекаю натискання клавіші...")
    key_label.update()

    try:
        def on_press(event):
            global selected_key
            key_name = event.name

            if key_name in UKR_TO_LAT:
                key_name = UKR_TO_LAT[key_name]

            selected_key = key_name
            save_key(selected_key)
            key_label.config(text=f"Обрана клавіша: {selected_key}")
            keyboard.unhook_all()
            log_message(f"Обрано клавішу: {selected_key}")

        keyboard.on_press(on_press)
    except Exception as e:
        key_label.config(text=f"Помилка: {e}")
        log_message(f"Помилка вибору клавіші: {e}")