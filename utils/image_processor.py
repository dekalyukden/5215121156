import cv2
from utils.logger import log_message

def select_region(event, x, y, flags, param):
    global x_start, y_start, x_end, y_end, cropping, image, image_copy, selected_key

    if event == cv2.EVENT_LBUTTONDOWN and selected_key is not None:
        x_start, y_start = x, y
        cropping = True
        log_message(f"Початок виділення: ({x_start}, {y_start})")
        image_copy = image.copy()

    elif event == cv2.EVENT_LBUTTONUP and selected_key is not None:
        x_end, y_end = x, y
        cropping = False
        cv2.rectangle(image, (x_start, y_start), (x_end, y_end), (0, 255, 0), 2)
        cv2.imshow("Screen", image)
        log_message(f"Кінець виділення: ({x_end}, {y_end})")

        print("Координати виділеної області:")
        print(f"x_start: {x_start}, y_start: {y_start}")
        print(f"x_end: {x_end}, y_end: {y_end}")
        log_message(f"Координати: ({x_start}, {y_start}), ({x_end}, {y_end})")

    elif event == cv2.EVENT_MOUSEMOVE and cropping and selected_key is not None:
        cv2.rectangle(image_copy, (x_start, y_start), (x, y), (0, 255, 0), 2)
        cv2.imshow("Screen", image_copy)
        image_copy = image.copy()