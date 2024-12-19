
import pyautogui
import pytesseract
import cv2
import numpy as np
from PIL import Image

# Configuración de la ruta de Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def find_word_on_screen(word_to_find, screenshot=None, coordenada1=(0, 0), coordenada2=(0, 0)):
    """
    Busca una palabra específica en una región delimitada de la pantalla o en una captura pasada.

    :param word_to_find: Palabra a buscar.
    :param screenshot: Captura de pantalla proporcionada (opcional).
    :param coordenada1: Esquina superior izquierda de la región (x1, y1).
    :param coordenada2: Esquina inferior derecha de la región (x2, y2).
    :return: Coordenadas (x, y) de la palabra encontrada o None si no se encuentra.
    """
    x1, y1 = coordenada1
    x2, y2 = coordenada2
    width = x2 - x1
    height = y2 - y1

    # Captura la región si no se proporciona una captura
    if screenshot is None:
        print("Capturando la región especificada...")
        screenshot = pyautogui.screenshot(region=(x1, y1, width, height))
    else:
        # Convertir de NumPy (OpenCV) a formato PIL si es necesario
        if isinstance(screenshot, np.ndarray):
            screenshot = Image.fromarray(cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB))
        elif not isinstance(screenshot, Image.Image):
            raise TypeError("La captura debe ser una imagen PIL o un array NumPy válido.")

    # Convertir la imagen a formato NumPy y RGB
    screenshot_np = np.array(screenshot)
    screenshot_rgb = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2RGB)

    # Realiza el OCR sobre la captura
    data = pytesseract.image_to_data(screenshot_rgb, output_type=pytesseract.Output.DICT,lang="spa")

    # Busca la palabra en los datos obtenidos
    for i, text in enumerate(data['text']):

        if text.strip() and word_to_find.lower() in text.lower():
            x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
            center_x = x1 + x + w // 2
            center_y = y1 + y + h // 2
            print(f"Palabra encontrada en: ({center_x}, {center_y})")
            return center_x, center_y

    print(f"No se encontró la palabra '{word_to_find}' en la región especificada.")
    return None



"""
import time

# Ejemplo de uso
time.sleep(4)  # Pausa para preparar la pantalla

# Cargar la imagen desde un archivo
capture = cv2.imread('../capture.png')
if capture is None:
    print("Error: No se pudo cargar la imagen. Verifica la ruta y el nombre del archivo.")
else:
    # Buscar la palabra "Cursor" en la captura y región especificada
    result = find_word_on_screen("DALL-E", capture, coordenada1=(505, 167), coordenada2=(1192, 360))

    if result:
        print(f"Coordenadas de la palabra: {result}")
    else:
        print("Palabra no encontrada.")
"""