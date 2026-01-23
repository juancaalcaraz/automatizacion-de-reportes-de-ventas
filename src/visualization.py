import os
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick 
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import numpy as np
import pandas as pd

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

def plot_forecast_holt_winters(df, figures_dir, horizon=3):
    """
    Genera pronóstico Holt-Winters con bandas de confianza (formato gerencial).

    Parámetros:
    df : pd.DataFrame
        Columnas: 'indice_tiempo', 'ventas_totales_canal_venta'
    figures_dir : str
        Carpeta donde se guarda el gráfico
    horizon : int
        Meses a pronosticar
    """

    os.makedirs(figures_dir, exist_ok=True)

    # --- Preparar serie de tiempo ---
    ts = (
        df.sort_values("indice_tiempo")
          .set_index("indice_tiempo")["ventas_totales_canal_venta"]
    )

    ts.index = pd.to_datetime(ts.index)
    ts = ts.asfreq("MS")
    ts = ts.dropna()

    # ================================
    # ESCALADO A MILES DE MILLONES
    # ================================
    scale = 1e9
    ts_scaled = ts / scale

    # --- Modelo Holt-Winters ---
    model = ExponentialSmoothing(
        ts_scaled,
        trend="add",
        seasonal="add",
        seasonal_periods=12
    )

    fit = model.fit(optimized=True)

    # --- Forecast ---
    forecast_scaled = fit.forecast(horizon)

    # --- Error histórico (RMSE) ---
    residuals = ts_scaled - fit.fittedvalues
    rmse = np.sqrt(np.mean(residuals**2))

    # --- Intervalos de confianza ---
    upper_scaled = forecast_scaled + 1.96 * rmse
    lower_scaled = forecast_scaled - 1.96 * rmse

    # --- Reescalar a valores reales ---
    forecast = forecast_scaled * scale
    lower = lower_scaled * scale
    upper = upper_scaled * scale

    # ================================
    # GRÁFICO (FORMATO GERENCIAL)
    # ================================
    plt.figure(figsize=(11, 5))

    plt.plot(ts.index, ts.values / scale, 
             label="Ventas reales", color="black")

    plt.plot(fit.fittedvalues.index, fit.fittedvalues.values, 
             label="Ajuste Holt-Winters", color="green")

    plt.plot(forecast.index, forecast.values / scale,
             label=f"Pronóstico ({horizon} meses)",
             linestyle="--", color="red")

    plt.fill_between(
        forecast.index,
        lower.values / scale,
        upper.values / scale,
        color="red",
        alpha=0.2,
        label="Intervalo de confianza (95%)"
    )

    plt.title("Proyección de Ventas Totales")
    plt.xlabel("Fecha")
    plt.ylabel("Ventas (miles de millones)")
    plt.legend()
    plt.grid(alpha=0.3)

    ax = plt.gca()

    # Formato eje Y → miles de millones (B)
    ax.ticklabel_format(style="plain", axis="y")
    ax.get_yaxis().get_offset_text().set_visible(False)
    ax.yaxis.set_major_formatter(
        mtick.FuncFormatter(lambda x, _: f"{x:.1f} B")
    )

    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, "forecast_hw.png"), dpi=150)
    plt.close()

    # ================================
    # EXPORTAR A EXCEL
    # ================================
    forecast_df = forecast.reset_index()
    forecast_df.columns = ["Mes", "Proyección total de ventas"]

    forecast_df["Proyección total de ventas"] = (
        forecast_df["Proyección total de ventas"]
        .round(0)
        .astype("int64")
    )

    forecast_df.to_excel(
        "outputs/forecast.xlsx",
        index=False
    )

    return forecast, lower, upper


