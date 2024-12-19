import os
import time
import threading
import keyboard
import pyautogui
import cv2
from PIL import Image
from dotenv import load_dotenv
from tools.movimiento_curvado import movimiento_curvado
from tools.find_word_on_screen import find_word_on_screen
import google.generativeai as genai

# Configuración de entorno
load_dotenv()
API_KEY = os.getenv("Gemini")
if not API_KEY:
    raise ValueError("Error: API_KEY no encontrada en el archivo .env.")
genai.configure(api_key=API_KEY)

# Constantes
HOTKEY = "Ctrl+1"  # Atajo para procesar texto
CLOSE_KEY = "Ctrl+2"  # Atajo para cerrar el script
MODEL = "gpt-4o-mini"
threads = []  # Lista global para rastrear hilos activos

# Variables para almacenar las esquinas
corner1 = None
corner2 = None

# Funciones de utilidad
def get_mouse_position():
    """Obtiene las coordenadas actuales del mouse."""
    x, y = pyautogui.position()
    return x, y

def capture_window(x1, y1, x2, y2):
    """Captura una región definida por dos esquinas y guarda como 'capture.png'."""
    ancho, alto = x2 - x1, y2 - y1
    image_path = "capture.png"
    captura = pyautogui.screenshot(region=(x1, y1, ancho, alto))
    captura.save(image_path)
    print("¡La captura de la ventana fue exitosa!")
    return image_path

def process_image_with_prompt(image_path, prompt):
    """Procesa la imagen con un prompt y devuelve la respuesta."""
    try:
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Imagen no encontrada: {image_path}")

        Image.open(image_path).verify()
        print(f"Imagen '{image_path}' abierta correctamente.")

        uploaded_file = genai.upload_file(path=image_path, display_name=os.path.basename(image_path))
        print(f"Archivo subido con URI: {uploaded_file.uri}")

        model = genai.GenerativeModel(model_name="gemini-1.5-pro")
        response = model.generate_content([uploaded_file, prompt])
        return response.text
    except Exception as e:
        print(f"Error al procesar la imagen con Gemini: {e}")
        return None

def mover_a_answer(x, y):
    """Mueve el cursor hacia las coordenadas absolutas especificadas."""
    if x is not None and y is not None:
        print(f"Moviendo el cursor a: ({x}, {y})")
        movimiento_curvado(x, y, 800, 4)
    else:
        print("Coordenadas inválidas. No se puede mover el cursor.")

def on_close():
    """Finaliza el script y cierra de forma segura los hilos activos."""
    print(f"Cerrando el script con {CLOSE_KEY}. Espera a que los hilos finalicen...")
    for thread in threads:
        if thread.is_alive():
            print(f"Esperando hilo {thread.name}...")
            thread.join()
    print("Todos los hilos finalizados. Cerrando el programa.")
    os._exit(0)

def handle_capture():
    """Maneja la captura de las esquinas seleccionadas."""
    global corner1, corner2

    if corner1 is None:
        corner1 = get_mouse_position()
        print(f"Primer punto capturado: {corner1}")
    elif corner2 is None:
        corner2 = get_mouse_position()
        print(f"Segundo punto capturado: {corner2}")
        process_capture()
    else:
        print("Ambos puntos ya han sido capturados.")

def process_capture():
    """Procesa la captura de pantalla y ejecuta el flujo completo."""
    global corner1, corner2

    if corner1 and corner2:
        x1, y1 = corner1
        x2, y2 = corner2

        print("Tomando la captura de pantalla de la región seleccionada...")
        image_path = capture_window(x1, y1, x2, y2)

        prompt = "En esta imagen quiero que me respondas solo una palabra de la respuesta, si tiene caracteres especiales retorna una parte de la palabra."

        # Procesar la imagen con el prompt
        response = process_image_with_prompt(image_path, prompt)

        if response:
            print("Respuesta de Gemini:")
            print(response)
            try:
                img_cv2 = cv2.imread(image_path)
                if img_cv2 is None:
                    raise FileNotFoundError(f"Imagen no cargada: {image_path}")
                x, y = find_word_on_screen(response, img_cv2, (x1, y1), (x2, y2))
                mover_a_answer(x, y)
            except Exception as e:
                print(f"No se pudieron extraer coordenadas: {e}")
        else:
            print("No se pudo procesar la imagen.")

        # Resetear las esquinas
        corner1 = None
        corner2 = None
    else:
        print("Esquinas no definidas correctamente.")

def on_hotkey():
    """Inicia el proceso de captura de esquinas al presionar el atajo."""
    handle_capture()

# Programa principal
def main():
    """Configura los atajos y gestiona la espera de eventos del teclado."""
    print(f"Presiona {HOTKEY} para capturar las esquinas.")
    print(f"Presiona {CLOSE_KEY} para cerrar el programa.")

    keyboard.add_hotkey(HOTKEY, on_hotkey)
    keyboard.add_hotkey(CLOSE_KEY, on_close)

    # Esperar indefinidamente eventos del teclado
    keyboard.wait()

if __name__ == "__main__":
    main()
