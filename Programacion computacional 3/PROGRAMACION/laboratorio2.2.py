# EJERCICIO 3: PLATILLO MÁS VENDIDO (CORTO)

ventas = {}
n = int(input("¿Cuántos platillos se vendieron hoy?: "))

# Captura de platillos y conteo de repeticiones
for _ in range(n):
    p = input("Nombre del platillo: ").strip().capitalize()
    ventas[p] = ventas.get(p, 0) + 1

# Determina el más vendido y maneja empates
if ventas:
    max_v = max(ventas.values())
    mas_vendidos = [k for k, v in ventas.items() if v == max_v]
    print(f"\nMás vendido(s) con {max_v} ventas: {', '.join(mas_vendidos)}")