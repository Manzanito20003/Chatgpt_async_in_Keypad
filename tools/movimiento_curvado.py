from pynput.mouse import Controller
import time
import math

# Controlador del mouse
mouse = Controller()

def movimiento_curvado(dest_x, dest_y, pasos=50, duracion=1):
    """
    Mueve el mouse al destino siguiendo una trayectoria curva.
    :param dest_x: Coordenada X del destino.
    :param dest_y: Coordenada Y del destino.
    :param pasos: Número de puntos intermedios.
    :param duracion: Tiempo total del movimiento.
    """
    # Posición inicial del mouse
    inicio_x, inicio_y = mouse.position

    # Dividir el tiempo entre los pasos
    tiempo_por_paso = duracion / pasos

    for i in range(1, pasos + 1):
        # Usar una función curva (por ejemplo, seno) para suavizar
        inter_x = inicio_x + (dest_x - inicio_x) * (i / pasos)
        inter_y = inicio_y + (dest_y - inicio_y) * (i / pasos) + 10 * math.sin(i / pasos * math.pi)

        # Mover el mouse a la posición intermedia
        mouse.position = (inter_x, inter_y)
        time.sleep(tiempo_por_paso)

"""
time.sleep(3)
movimiento_curvado(945,548)
"""