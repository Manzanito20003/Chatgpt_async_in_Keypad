import pyautogui
import time

def track_mouse_position():
    """
    Muestra la posición del mouse en tiempo real en la consola.
    Presiona Ctrl+C para detener la ejecución.
    """
    try:
        print("Mueve el mouse para ver sus coordenadas. Presiona Ctrl+C para salir.\n")
        while True:
            # Obtén la posición actual del mouse
            x, y = pyautogui.position()
            print(f"Posición del mouse: x={x}, y={y}", end="\r")  # Sobrescribe la línea en la consola
            time.sleep(0.05)  # Actualiza cada 50 ms
    except KeyboardInterrupt:
        print("\nDetenido por el usuario.")


# Ejecutar la función
track_mouse_position()
