import os
import matplotlib.pyplot as plt
"""
def plot_sales(df, figures_dir):
    os.makedirs(figures_dir, exist_ok=True)

    plt.figure(figsize=(10, 5))
    plt.plot(df['indice_tiempo'], df['ventas_precios_corrientes'],
             label='Precios corrientes')
    plt.plot(df['indice_tiempo'], df['ventas_precios_constantes'],
             label='Precios constantes')
    plt.legend()
    plt.title("Ventas en supermercados")
    plt.tight_layout()

    plt.savefig(os.path.join(figures_dir, "ventas_totales.png"))
    plt.close()
"""
import os
import matplotlib.pyplot as plt

def plot_sales(df, figures_dir):
    """
    Genera gráficos principales para el reporte ejecutivo:
    - Ventas totales mensuales
    - Medios de pago (último mes)
    - Serie histórica de categorías
    Guarda los gráficos en figures_dir y devuelve un diccionario con los paths.
    """
    os.makedirs(figures_dir, exist_ok=True)
    paths = {}

    # Ventas totales
    plt.figure(figsize=(10,5))
    plt.plot(df['indice_tiempo'], df['ventas_totales_canal_venta'], marker='o')
    plt.title("Ventas Totales Mensuales")
    plt.xlabel("Fecha")
    plt.ylabel("Ventas (pesos)")
    plt.grid(True)
    plt.tight_layout()
    ventas_path = os.path.join(figures_dir, "ventas_totales.png")
    plt.savefig(ventas_path)
    plt.close()
    paths['ventas_totales'] = ventas_path

    # Medios de pago
    last = df.iloc[-1]
    valores = [last['efectivo'], last['tarjetas_debito'], last['tarjetas_credito'], last['otros']]
    labels = ['Efectivo', 'Débito', 'Crédito', 'Otros']
    plt.figure(figsize=(6,6))
    plt.pie(valores, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.title("Distribución de Medios de Pago")
    medios_path = os.path.join(figures_dir, "medios_pago.png")
    plt.savefig(medios_path)
    plt.close()
    paths['medios_pago'] = medios_path

    # Serie histórica de categorías
    categorias = ['almacen', 'panaderia', 'lacteos', 'carnes']
    plt.figure(figsize=(10,5))
    for cat in categorias:
        plt.plot(df['indice_tiempo'], df[cat], label=cat)
    plt.title("Ventas por Categoría")
    plt.xlabel("Fecha")
    plt.ylabel("Ventas (pesos)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    serie_path = os.path.join(figures_dir, "serie_historica.png")
    plt.savefig(serie_path)
    plt.close()
    paths['serie_historica'] = serie_path

    return paths
