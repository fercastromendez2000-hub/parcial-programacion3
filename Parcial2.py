import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QComboBox, QLabel, QTabWidget,
    QHeaderView, QMessageBox
)
from PyQt5.QtCore import Qt

class AnalizadorInventario:
    """Clase encargada de la manipulación e inspección de datos con Pandas."""
    def __init__(self, ruta_csv='datos.csv'):
        self.ruta_csv = ruta_csv
        self.df = self.cargar_datos()

    def cargar_datos(self):
        try:
            df = pd.read_csv(self.ruta_csv)
            # Calculamos el valor total en dólares por registro
            df['valor_inventario'] = df['cantidad_stock'] * df['precio_unitario']
            return df
        except Exception as e:
            print(f"Error al cargar el archivo CSV: {e}")
            return pd.DataFrame()

    def obtener_inspeccion_consola(self):
        """Muestra en consola las funciones de inspección requeridas por el parcial."""
        print("=== 1. ESTRUCTURA Y PRIMEROS REGISTROS ===")
        print(self.df.head())
        print("\n=== 2. INFORMACIÓN GENERAL Y TIPOS DE DATOS ===")
        print(self.df.info())
        print("\n=== 3. ESTADÍSTICAS BÁSICAS DE VARIABLES NUMÉRICAS ===")
        print(self.df.describe())
        print("\n=== 4. TOTALES POR SUCURSAL ===")
        print(self.df.groupby('sucursal')[['cantidad_stock', 'valor_inventario']].sum())

class CanvasGrafico(FigureCanvas):
    """Componente para renderizar gráficos de Matplotlib dentro de PyQt5."""
    def __init__(self, parent=None):
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        super().__init__(self.fig)
        self.setParent(parent)

class VentanaPrincipal(QMainWindow):
    def __init__(self, analizador):
        super().__init__()
        self.analizador = analizador
        self.df = analizador.df
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Sistema de Gestión de Inventarios - Consultoría de Datos")
        self.setGeometry(100, 100, 1100, 700)

        # Widget central con pestañas
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Creación de pestañas
        self.tab_tabla = QWidget()
        self.tab_graficos = QWidget()

        self.tabs.addTab(self.tab_tabla, "📋 Vista de Datos")
        self.tabs.addTab(self.tab_graficos, "📊 Visualización y Gráficos")

        self.setup_tab_tabla()
        self.setup_tab_graficos()

    def setup_tab_tabla(self):
        layout = QVBoxLayout()

        # Filtro de Sucursal
        filtro_layout = QHBoxLayout()
        filtro_layout.addWidget(QLabel("Filtrar por Sucursal:"))
        self.combo_sucursal = QComboBox()
        self.combo_sucursal.addItem("Todas")
        self.combo_sucursal.addItems(sorted(self.df['sucursal'].unique().tolist()))
        self.combo_sucursal.currentTextChanged.connect(self.filtrar_tabla)
        filtro_layout.addWidget(self.combo_sucursal)
        filtro_layout.addStretch()

        layout.addLayout(filtro_layout)

        # Tabla de Datos
        self.tabla = QTableWidget()
        layout.addWidget(self.tabla)

        self.tab_tabla.setLayout(layout)
        self.cargar_tabla_datos(self.df)

    def cargar_tabla_datos(self, dataframe):
        self.tabla.setRowCount(dataframe.shape[0])
        self.tabla.setColumnCount(dataframe.shape[1])
        self.tabla.setHorizontalHeaderLabels(dataframe.columns)

        for i in range(dataframe.shape[0]):
            for j in range(dataframe.shape[1]):
                val = dataframe.iloc[i, j]
                # Formato a números flotantes para columnas financieras/precios
                if isinstance(val, float) and j >= 4:
                    val = f"${val:,.2f}"
                self.tabla.setItem(i, j, QTableWidgetItem(str(val)))

        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def filtrar_tabla(self, sucursal):
        if sucursal == "Todas":
            self.cargar_tabla_datos(self.df)
        else:
            df_filtrado = self.df[self.df['sucursal'] == sucursal]
            self.cargar_tabla_datos(df_filtrado)

    def setup_tab_graficos(self):
        layout = QVBoxLayout()

        # Contenedor de gráficos (2 canvas lado a lado)
        graficos_layout = QHBoxLayout()

        self.canvas_barras = CanvasGrafico(self)
        self.canvas_pie = CanvasGrafico(self)

        graficos_layout.addWidget(self.canvas_barras)
        graficos_layout.addWidget(self.canvas_pie)

        layout.addLayout(graficos_layout)
        self.tab_graficos.setLayout(layout)

        self.generar_graficos()

    def generar_graficos(self):
        # Gráfico 1: Valor total del inventario por Sucursal (Barras)
        resumen_sucursal = self.df.groupby('sucursal')['valor_inventario'].sum().reset_index()
        
        self.canvas_barras.ax.clear()
        self.canvas_barras.ax.bar(resumen_sucursal['sucursal'], resumen_sucursal['valor_inventario'], color='#2b5c8f')
        self.canvas_barras.ax.set_title("Valor Total de Inventario por Sucursal ($)", fontsize=11, fontweight='bold')
        self.canvas_barras.ax.set_ylabel("Monto ($)")
        self.canvas_barras.ax.tick_params(axis='x', rotation=30)
        self.canvas_barras.fig.tight_layout()
        self.canvas_barras.draw()

        # Gráfico 2: Distribución de Stock por Categoría (Pie Chart)
        resumen_cat = self.df.groupby('categoria')['cantidad_stock'].sum()
        
        self.canvas_pie.ax.clear()
        self.canvas_pie.ax.pie(resumen_cat, labels=resumen_cat.index, autopct='%1.1f%%', colors=['#4c9be8', '#ff9f43'])
        self.canvas_pie.ax.set_title("Distribución de Unidades por Categoría", fontsize=11, fontweight='bold')
        self.canvas_pie.fig.tight_layout()
        self.canvas_pie.draw()

if __name__ == '__main__':
    # 1. Ejecutar inspección en consola (Criterio de Pandas)
    analizador = AnalizadorInventario('datos.csv')
    analizador.obtener_inspeccion_consola()

    # 2. Iniciar Aplicación Gráfica
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal(analizador)
    ventana.show()
    sys.exit(app.exec_())