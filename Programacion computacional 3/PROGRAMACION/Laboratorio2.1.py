# EJERCICIO 2: INVENTARIO EN BODEGA

# Inventario inicial
inv = {"Tomate": 10, "Cebolla": 15, "Carne": 8, "Queso": 12}

# Entrada de datos
n = int(input("¿Cuántos ingredientes sacará para la receta?: "))
pedidos = {input(f"Ingrediente {i+1}: ").strip().capitalize(): int(input("Cantidad: ")) for i in range(n)}

# Validación previa: Se verifica la disponibilidad de TODOS antes de descontar
if all(k in inv and inv[k] >= v for k, v in pedidos.items()):
    for k, v in pedidos.items():
        inv[k] -= v
    print("\n¡Éxito! Ingredientes retirados del inventario.")
else:
    print("\n[ERROR] No se pudo realizar el retiro. Cantidad supera lo disponible o el ingrediente no existe.")

# Reporte final
print("\n--- REPORTE DE INVENTARIO ACTUALIZADO ---")
for ingrediente, cantidad in inv.items():
    print(f"- {ingrediente}: {cantidad}")