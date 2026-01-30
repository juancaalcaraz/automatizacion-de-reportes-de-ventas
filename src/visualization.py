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


def plot_backtest_validation(ts_scaled, train, test, test_predictions, figures_dir):
    """
    Genera un gráfico comparando la predicción del backtest contra la realidad.
    """
    plt.figure(figsize=(10, 5))
    
    # Datos de entrenamiento
    plt.plot(train.index, train.values, label="Entrenamiento", color="black", alpha=0.5)
    
    # Comparativa: Real vs Predicho
    plt.plot(test.index, test.values, label="Real (Test)", color="blue", linewidth=2)
    plt.plot(test.index, test_predictions, label="Predicción Backtest", color="orange", linestyle="--", linewidth=2)
    
    plt.title("Validación de Modelo: Predicción vs Realidad (Últimos 12 meses)")
    plt.xlabel("Fecha")
    plt.ylabel("Ventas (Escaladas)")
    plt.legend()
    plt.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, "backtest_validation.png"), dpi=150)
    plt.close()
#Nueva función 
def plot_forecast_holt_winters(df, figures_dir, horizon=3):
    """
    Genera pronóstico Holt-Winters con validación (Backtesting) y bandas de confianza.
    """
    os.makedirs(figures_dir, exist_ok=True)

    # --- Preparar serie de tiempo ---
    ts = (
        df.sort_values("indice_tiempo")
          .set_index("indice_tiempo")["ventas_totales_canal_venta"]
    )
    ts.index = pd.to_datetime(ts.index)
    ts = ts.asfreq("MS").dropna()

    scale = 1e9
    ts_scaled = ts / scale

    # ==========================================
    # 1. BACKTESTING (Validación del modelo)
    # ==========================================
    # Reservamos los últimos 12 meses para testear la precisión
    train_size = len(ts_scaled) - 12
    train, test = ts_scaled.iloc[:train_size], ts_scaled.iloc[train_size:]

    model_backtest = ExponentialSmoothing(
        train, trend="add", seasonal="add", seasonal_periods=12
    ).fit(optimized=True)
    
    # Predecimos el periodo de test para calcular el error real
    test_predictions = model_backtest.forecast(len(test))
    rmse_backtest = np.sqrt(np.mean((test - test_predictions)**2))
    
    print(f"--- Validación finalizada ---")
    print(f"Registros totales: {len(ts_scaled)}")
    print(f"Operaciones en Backtest: {len(test)} meses")
    print(f"RMSE de validación: {rmse_backtest:.4f} B")
    # ... después de calcular test_predictions ...
    plot_backtest_validation(ts_scaled, train, test, test_predictions, figures_dir)
    # ==========================================
    # 2. PREDICCIÓN FINAL (Uso de todos los datos)
    # ==========================================
    # Ahora sí, entrenamos con el 100% para el futuro real
    final_model = ExponentialSmoothing(
        ts_scaled, trend="add", seasonal="add", seasonal_periods=12
    ).fit(optimized=True)

    forecast_scaled = final_model.forecast(horizon)
    
    # Usamos el RMSE del backtest para los intervalos (es más realista que el de ajuste)
    upper_scaled = forecast_scaled + 1.96 * rmse_backtest
    lower_scaled = forecast_scaled - 1.96 * rmse_backtest

    # Reescalar
    forecast = forecast_scaled * scale
    lower = lower_scaled * scale
    upper = upper_scaled * scale

    # ================================
    # GRÁFICO (FORMATO GERENCIAL)
    # ================================
    plt.figure(figsize=(11, 5))
    plt.plot(ts.index, ts.values / scale, label="Ventas reales", color="black", linewidth=1.5)
    plt.plot(final_model.fittedvalues.index, final_model.fittedvalues.values, 
             label="Ajuste histórico", color="green", alpha=0.6)
    
    plt.plot(forecast.index, forecast.values / scale,
             label=f"Pronóstico ({horizon} meses)", linestyle="--", color="red")

    plt.fill_between(forecast.index, lower.values / scale, upper.values / scale,
                     color="red", alpha=0.15, label="Intervalo de confianza (Backtest)")

    plt.title("Proyección de Ventas Totales (Validada vía Backtesting)")
    plt.xlabel("Fecha")
    plt.ylabel("Ventas (miles de millones)")
    plt.legend()
    plt.grid(alpha=0.3)

    ax = plt.gca()
    ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"{x:.1f} B"))

    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, "forecast_hw.png"), dpi=150)
    plt.close()

    # ================================
    # EXPORTAR A EXCEL (CON ESCENARIOS)
    # ================================
    # Creamos un DataFrame con el forecast y los intervalos
    forecast_df = pd.DataFrame({
        "Mes": forecast.index,
        "Ventas Escenario Mínimo": lower.values,
        "Proyección Ventas (Base)": forecast.values,
        "Ventas Escenario Máximo": upper.values
    })

    # Redondear y pasar a entero para un formato más limpio
    cols_a_formatear = [
        "Ventas Escenario Mínimo", 
        "Proyección Ventas (Base)", 
        "Ventas Escenario Máximo"
    ]
    
    for col in cols_a_formatear:
        forecast_df[col] = forecast_df[col].round(0).astype("int64")

    # Guardar en la carpeta de outputs
    os.makedirs("outputs", exist_ok=True)
    forecast_df.to_excel(
        "outputs/forecast_escenarios.xlsx", 
        index=False
    )

    print("✅ Excel exportado con escenarios Mínimo, Base y Máximo.")
    
    return forecast_df, lower, upper

