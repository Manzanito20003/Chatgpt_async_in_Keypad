def calcular_distancia(d, f):
    # Calcula la distancia según la fórmula
    rpta = d - (d * f) / (d - f)
    return round(rpta, 2)

# Entrada de datos
d = float(input("d: "))
f = float(input("f: "))

# Llamada a la función y resultado
resultado = calcular_distancia(d, f)
print(f"La distancia es {resultado} cm")
