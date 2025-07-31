# **Nombre del Proyecto**

Este proyecto permite realizar las siguientes tareas:  
1. Encontrar una palabra en una captura de pantalla y devolver su posición en coordenadas con ORC tesseract **(x, y)**.  
2. Realizar movimientos curvados hacia una posición con el mouse.  
3. Obtener la posición actual del mouse.
4. mandar a gemini 
## **Tabla de Contenidos**
- [Instalación](#instalación)
- [Uso](#uso)
- [Contribución](#contribución)
- [Licencia](#licencia)

---

## **Instalación**
Sigue estos pasos para instalar el proyecto en tu máquina local:

Necesitaras instalar ORC Tesstrack este motor para reconocimento de caracteres.

1. **Clona este repositorio**:
   ```bash
   git clone https://github.com/Manzanito20003/Chatgpt_async_in_Keypad.git
   ```
2. **Instala las dependencias** listadas en `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```
3. **Ejecuta el script** (ajusta el comando según el archivo que necesites):
   ```bash
   python tools/find_word_on_screen.py
   python tools/movimiento_curvado.py
   python tools/track_mouse_position.py
   ```

---

## **Uso**
### **1. Encontrar palabras en pantalla**
Ejecuta el script `find_word_on_screen.py` para buscar una palabra en una captura de pantalla y obtener su posición en coordenadas.

### **2. Mover el mouse con trayectoria curvada**
Ejecuta `movimiento_curvado.py` para mover el mouse de manera curvada hacia una posición específica.

### **3. Obtener la posición del mouse**
Ejecuta `track_mouse_position.py` para obtener y mostrar la posición actual del mouse.

---

## **Contribución**
¿Quieres contribuir? Sigue estos pasos:
1. Haz un **fork** del repositorio.
2. Crea una nueva rama con tu funcionalidad:
   ```bash
   git checkout -b feature/nueva-funcionalidad
   ```
3. Realiza tus cambios y haz un commit:
   ```bash
   git commit -m "Añadida nueva funcionalidad"
   ```
4. Sube tus cambios al repositorio remoto:
   ```bash
   git push origin feature/nueva-funcionalidad
   ```
5. Abre un **Pull Request**.

---

## **Licencia**
Este proyecto está bajo la licencia **MIT**. Consulta el archivo `LICENSE` para más detalles.
