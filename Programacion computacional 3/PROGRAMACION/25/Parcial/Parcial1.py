"""
Sistema de Gimnasio - Parcial de Primer Cómputo
Programación Computacional III
"""

def calcular_descuento(precio, porcentaje=10):
    """
    Calcula el precio final aplicando un descuento.
    Tiene un valor por defecto en 'porcentaje' (10%).
    """
    descuento = precio * (porcentaje / 100)
    precio_final = precio - descuento
    return precio_final


def validar_texto(mensaje):
    """
    Pide un texto al usuario y valida que no esté vacío.
    Maneja la excepción si algo falla al ingresar el dato.
    """
    while True:
        try:
            dato = input(mensaje).strip()
            if dato == "":
                raise ValueError("El campo no puede estar vacío.")
            return dato
        except ValueError as e:
            print(f"Error: {e}. Intente de nuevo.")

class Persona:
    def __init__(self, nombre, edad):
        self.nombre = nombre          # variable tipo str
        self.edad = edad              # variable tipo int

    def mostrar_info(self):
        print(f"Nombre: {self.nombre} | Edad: {self.edad} años")

    def es_mayor_edad(self):
        return self.edad >= 18

class Miembro(Persona):
    def __init__(self, nombre, edad, membresia="Mensual", activo=True):
        super().__init__(nombre, edad)
        self.membresia = membresia    # variable tipo str
        self.activo = activo          # variable tipo bool
        self.pagos = []                # lista -> agrupación de datos

    def registrar_pago(self, monto=25.0):
        """Método con valor por defecto en el parámetro monto."""
        self.pagos.append(monto)
        print(f"Pago de ${monto:.2f} registrado para {self.nombre}.")

    def mostrar_membresia(self):
        estado = "Activo" if self.activo else "Inactivo"
        total_pagado = sum(self.pagos)
        print(f"{self.nombre} | Membresía: {self.membresia} | "
              f"Estado: {estado} | Total pagado: ${total_pagado:.2f}")

def cargar_miembros_ejemplo():
    """Crea y retorna una lista con 5 miembros de ejemplo precargados."""
    miembros = [
        Miembro("Carlos Pérez", 25, "Mensual"),
        Miembro("Ana Gómez", 30, "Anual"),
        Miembro("Luis Martínez", 17, "Mensual", activo=False),
        Miembro("María López", 22, "Trimestral"),
        Miembro("Jorge Ramírez", 40, "Anual"),
    ]
    # Se les registra un pago inicial de ejemplo a cada uno
    miembros[0].registrar_pago(25.0)
    miembros[1].registrar_pago(200.0)
    miembros[2].registrar_pago(25.0)
    miembros[3].registrar_pago(70.0)
    miembros[4].registrar_pago(200.0)
    return miembros

def main():
    lista_miembros = cargar_miembros_ejemplo()  # lista con 5 miembros precargados
    print("Se cargaron 5 miembros de ejemplo al iniciar el sistema.")

    while True:
        print("\n===== MENÚ GIMNASIO =====")
        print("1. Registrar nuevo miembro")
        print("2. Registrar pago de un miembro")
        print("3. Ver todos los miembros")
        print("4. Calcular precio con descuento")
        print("5. Salir")

        opcion = input("Elija una opción: ").strip()

        if opcion == "1":
            nombre = validar_texto("Nombre del miembro: ")
            try:
                edad = int(input("Edad: "))
            except ValueError:
                print("Edad inválida, se asignará 18 por defecto.")
                edad = 18

            membresia = validar_texto("Tipo de membresía (Mensual/Anual): ")
            nuevo = Miembro(nombre, edad, membresia)
            lista_miembros.append(nuevo)
            print("Miembro registrado con éxito.")

        elif opcion == "2":
            if not lista_miembros:
                print("No hay miembros registrados.")
                continue
            for i, m in enumerate(lista_miembros):
                print(f"{i}. {m.nombre}")
            try:
                idx = int(input("Seleccione el número del miembro: "))
                monto = float(input("Monto a pagar (Enter para $25.00 por defecto): ") or 25.0)
                lista_miembros[idx].registrar_pago(monto)
            except (ValueError, IndexError):
                print("Error: dato inválido o miembro no existe.")

        elif opcion == "3":
            if not lista_miembros:
                print("No hay miembros registrados.")
            for m in lista_miembros:
                m.mostrar_info()
                m.mostrar_membresia()
                print(f"¿Es mayor de edad? {'Sí' if m.es_mayor_edad() else 'No'}")
                print("-" * 30)

        elif opcion == "4":
            try:
                precio = float(input("Precio original: "))
                usar_default = input("¿Usar descuento por defecto de 10%? (s/n): ").lower()
                if usar_default == "s":
                    final = calcular_descuento(precio)
                else:
                    porcentaje = float(input("Ingrese porcentaje de descuento: "))
                    final = calcular_descuento(precio, porcentaje)
                print(f"Precio final: ${final:.2f}")
            except ValueError:
                print("Error: debe ingresar un número válido.")

        elif opcion == "5":
            print("Saliendo del sistema. ¡Hasta luego!")
            break

        else:
            print("Opción no válida, intente de nuevo.")


if __name__ == "__main__":
    main()

# DESCRIPCIÓN DEL SISTEMA

# a. ¿Qué hace el sistema?
#    Es un pequeño programa para llevar el control de un gimnasio: se pueden
#    registrar miembros, anotar sus pagos y ver un resumen de cada uno desde
#    un menú simple.
#
# b. Clases que usamos:
#    - Persona: datos básicos de una persona (nombre y edad).
#    - Miembro: un cliente del gimnasio. Hereda de Persona y le suma
#      su membresía y sus pagos.
#
# c. Cada clase por dentro:
#    - Persona
#        Tiene: nombre, edad
#        Hace: mostrar_info() (imprime nombre y edad),
#              es_mayor_edad() (dice si es mayor de edad)
#    - Miembro (hereda de Persona)
#        Tiene: membresia, activo, pagos
#        Hace: registrar_pago() (guarda un pago, por defecto $25),
#              mostrar_membresia() (muestra membresía, estado y total pagado)
