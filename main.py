import openai
import pyperclip
import keyboard
from dotenv import load_dotenv
import threading
import re
from os import getenv

# Configuración
load_dotenv()  # Cargar variables desde .env si es necesario

key=getenv("API_KEY")
openai.api_key = key
HOTKEY = "ctrl+1"  # Atajo para procesar texto
CLOSE_KEY = "ctrl+2"  # Atajo para cerrar el script
MODEL = "gpt-4o-mini"  # Modelo de OpenAI

# Lista global para rastrear hilos activos
threads = []

#suma d 3 numerso
def on_close():
    """
    Finaliza el script y cierra de forma segura los hilos activos.
    """
    print(f"Cerrando el script con {CLOSE_KEY}. Espera a que los hilos finalicen...")
    for thread in threads:
        if thread.is_alive():
            print(f"Esperando hilo {thread.name}...")
            thread.join()  # Esperar que el hilo termine
    print("Todos los hilos finalizados. Cerrando el programa.")
    os._exit(0)  # Fuerza el cierre del programa


def get_selected_text():
    """
    Obtiene y limpia el texto seleccionado en el portapapeles.
    :return: Texto seleccionado limpio o None si está vacío.
    """
    text = pyperclip.paste().strip()
    return " ".join(text.split()) if text else None  # Limpia espacios múltiples


def send_to_gpt_prompt(prompt):
    """
    Envía el texto a la API de GPT y obtiene la respuesta.
    :param prompt: Texto ingresado por el usuario.
    :return: Respuesta generada por GPT o un mensaje de error.
    """
    prompt = (
        "Genera codigo phytom para :"
        + prompt
        + ". Además, recuerda darme el código bien ordenado y sin descripciones."
    )
    try:
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        return response['choices'][0]['message']['content']


    except openai.error.OpenAIError as e:
        print(f"Error al conectar con GPT: {e}")
        return "Error al procesar la solicitud."
    except Exception as e:
        print(f"Error inesperado: {e}")
        return "Error inesperado."






def extract_matlab_code(response):
    """
    Extrae el bloque de código MATLAB de la respuesta GPT.
    :param response: Respuesta completa generada por GPT.
    :return: Código MATLAB extraído o un mensaje indicando que no se encontró código.
    """
    match = re.search(r"```python(.*?)```", response, re.DOTALL)
    return match.group(1).strip() if match else "No se encontró un bloque de código MATLAB en la respuesta."

def handle_text_selection():
    """
    Maneja la lógica para enviar texto seleccionado a GPT, extraer el código MATLAB y copiarlo al portapapeles.
    """
    selected_text = get_selected_text()
    if not selected_text:
        print("No se encontró texto válido en el portapapeles. Asegúrate de copiarlo con Ctrl+C.")
        return

    print(f"Texto seleccionado: {selected_text}")
    response = send_to_gpt_prompt(selected_text)
    print(f"Respuesta de GPT completa:\n{response}")

    matlab_code = extract_matlab_code(response)
    pyperclip.copy(matlab_code)
    print("Código MATLAB copiado al portapapeles.")


def on_hotkey():
    """
    Inicia un hilo para procesar texto cuando se detecta el atajo de teclado.
    """
    print(f"Atajo detectado: {HOTKEY}")
    thread = threading.Thread(target=handle_text_selection, name=f"Hilo-{len(threads) + 1}")
    thread.start()
    threads.append(thread)


def main():
    """
    Configura los atajos y gestiona la espera de eventos del teclado.
    """
    print(f"Presiona {HOTKEY} después de seleccionar y copiar texto para enviarlo a GPT.")
    print(f"Presiona {CLOSE_KEY} para cerrar el programa.")

    # Registrar los atajos
    keyboard.add_hotkey(HOTKEY, on_hotkey)
    keyboard.add_hotkey(CLOSE_KEY, on_close)

    # Esperar indefinidamente eventos del teclado
    keyboard.wait()


if __name__ == "__main__":
    if not openai.api_key or openai.api_key == "tu_api_key_aqui":
        print("Error: No se ha configurado una clave de API válida.")
        os._exit(1)  # Cierra el programa si no hay API key configurada
    main()
