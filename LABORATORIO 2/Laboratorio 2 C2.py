import pandas as pd
import matplotlib.pyplot as plt

dt = pd.read_csv('ConsumoElectrico.csv')

print(dt.head())
print(dt.info())
print(dt.describe())

#Grafico 1
plt.figure(figsize=(10, 6))

for pais, datos in dt.groupby('Pais'):
    plt.plot(datos['Anio'], datos['Consumo_GWh'], label=pais, marker='o', linewidth=2)

plt.title("Evolución del Consumo de Energía Eléctrica (2015-2025)", fontsize=14)
plt.xlabel("Año", fontsize=12)
plt.ylabel("Consumo (GWh)", fontsize=12)
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend(title="País")
plt.tight_layout()

plt.savefig("Consumo_Energia_Electrica.png", dpi=300)
plt.show()

#Grafico 2
plt.figure(figsize=(10, 6))
for pais, datos in dt.groupby('Pais'):
    plt.bar(datos['Anio'], datos['Consumo_GWh'], label=pais, alpha=0.7)

plt.title("Consumo de Energía Eléctrica por País (2015-2025)", fontsize=14)
plt.xlabel("Año", fontsize=12)
plt.ylabel("Consumo (GWh)", fontsize=12)
plt.grid(axis='y', linestyle="--", alpha=0.6)
plt.legend(title="País")
plt.tight_layout()

plt.savefig("Consumo_Energia_Electrica(Barras).png", dpi=300)
plt.show()