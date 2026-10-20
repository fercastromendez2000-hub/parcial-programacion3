# EJERCICIO 4: EMPLEADOS (POO ULTRA CORTO)

class Empleado:
    def __init__(self, n, e, m, s): self.n, self.e, self.m, self.s = n, e, m, s
    def info(self): print(f"{self.n} ({self.e}añ) | Meses: {self.m} | Total: ${self.s + (self.s * 0.1 * (self.m // 12)):.2f}")

class Cocinero(Empleado):
    def __init__(self, n, e, m, s, esp): super().__init__(n, e, m, s); self.esp = esp
    def info(self): super().info(); print(f"Cocinero - Especialidad: {self.esp}")

class Mesero(Empleado):
    def __init__(self, n, e, m, s, tur): super().__init__(n, e, m, s); self.tur = tur
    def info(self): super().info(); print(f"Mesero - Turno: {self.tur}")

t = input("Tipo (C/M): ").upper()
nom, ed, ms, sal = input("Nombre: "), int(input("Edad: ")), int(input("Meses: ")), float(input("Salario: "))

if t == "C": emp = Cocinero(nom, ed, ms, sal, input("Especialidad: "))
else:
    tur = input("Turno (matutino/vespertino): ").lower()
    while tur not in ["matutino", "vespertino"]: tur = input("Error. Turno: ").lower()
    emp = Mesero(nom, ed, ms, sal, tur)

emp.info()