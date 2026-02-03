import os
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick 
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import numpy as np
import pandas as pd
from statsmodels.tsa.exponential_smoothing.ets import ETSModel # Nuevo import

####################################################
# esta función ya no se usa pero quedo como legacy #
####################################################
def plot_backtest_validation_1(ts_scaled, train, test, test_predictions, figures_dir):
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
####################################################
# esta función ya no se usa pero quedo como legacy #
####################################################
def plot_forecast_holt_winters_1(df, figures_dir,output_forecast, horizon=3):
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
        output_forecast, 
        index=False
    )

    print("✅ Excel exportado con escenarios Mínimo, Base y Máximo.")
    
    return forecast_df, lower, upper
# Tratando nuevamente con etsMoldes           

def plot_backtest_validation(ts_scaled, train, test, test_predictions, figures_dir):
    plt.figure(figsize=(10, 5))
    plt.plot(train.index, train.values, label="Entrenamiento", color="black", alpha=0.5)
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
# Aunque dice holt_winters, en realidad es ETSModels.
def plot_forecast_holt_winters(df, figures_dir, output_forecast, horizon=3):
    
    os.makedirs(figures_dir, exist_ok=True)
    #print("Cargando df y transormar a ts")
    # --- Preparar serie de tiempo ---
    ts = (
        df.sort_values("indice_tiempo")
          .set_index("indice_tiempo")["ventas_totales_canal_venta"]
    )
    ts.index = pd.to_datetime(ts.index)
    ts = ts.asfreq("MS").dropna()

    scale = 1e9 #Antes 1e9
    ts_scaled = ts / scale
    ts_scaled.dropna(inplace=True)
    #print("Cargado ts")
    # ==========================================
    # 1. BACKTESTING (Validación con ETSModel)
    # ==========================================
    import traceback
    train_size = len(ts_scaled) - 12
    train, test = ts_scaled.iloc[:train_size], ts_scaled.iloc[train_size:]
    train = train.astype('float64')

    #print(f"Iniciando modelo, {train}.")
    try:
        #print("Entrando al fit...")
        model_backtest = ETSModel(
            train, error="add", trend="add", seasonal="add", seasonal_periods=12,
            initialization_method="heuristic" 
        ).fit(
            # Eliminamos opt_kwargs y usamos parámetros directos de L-BFGS si son necesarios
            disp=False 
        )
        #print("Fit finalizado con éxito.")
    except Exception as e:
        import traceback
        traceback.print_exc()
        return None
    
    #print("Obteniendo backtest")
    # Obtenemos la predicción puntual del backtest
    test_predictions = model_backtest.forecast(len(test))
    rmse_backtest = np.sqrt(np.mean((test - test_predictions)**2))
    #print("Lllamando función plot")
    plot_backtest_validation(ts_scaled, train, test, test_predictions, figures_dir)

    # ==========================================
    # 2. PREDICCIÓN FINAL CON RANGOS
    # ==========================================
    # Parte 2: PREDICCIÓN FINAL
    final_model = ETSModel(
        ts_scaled, error="add", trend="add", seasonal="add", seasonal_periods=12,
        initialization_method="heuristic" # <--- Añade esto aquí también
    ).fit(disp=False)

    # Usamos get_prediction para obtener intervalos de confianza
    # alpha=0.05 equivale a un intervalo del 95%
    forecast_res = final_model.get_prediction(start=len(ts_scaled), end=len(ts_scaled) + horizon - 1)
    
    # Extraemos el DataFrame resumen con las bandas
    summary_frame = forecast_res.summary_frame(alpha=0.05)
    
    # Reescalar resultados
    forecast_scaled = summary_frame["mean"]
    lower_scaled = summary_frame["pi_lower"]
    upper_scaled = summary_frame["pi_upper"]

    forecast = forecast_scaled * scale
    lower = lower_scaled * scale
    upper = upper_scaled * scale

    # ================================
    # GRÁFICO (FORMATO GERENCIAL)
    # ================================
    plt.figure(figsize=(11, 5))
    plt.plot(ts.index, ts.values / scale, label="Ventas reales", color="black", linewidth=1.5)
    
    # Graficar predicción y bandas
    plt.plot(forecast.index, forecast.values / scale,
             label=f"Pronóstico ({horizon} meses)", linestyle="--", color="red")

    plt.fill_between(forecast.index, lower.values / scale, upper.values / scale,
                     color="red", alpha=0.15, label="Escenario de Riesgo (95% Confianza)")

    plt.title("Proyección Estratégica de Ventas (Modelo ETS)")
    plt.xlabel("Fecha")
    plt.ylabel("Ventas (miles de millones)")
    plt.legend()
    plt.grid(alpha=0.3)

    ax = plt.gca()
    ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"{x:.1f} B"))

    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, "forecast_ets.png"), dpi=150)
    plt.close()

    # ================================
    # EXPORTAR A EXCEL (ESCENARIOS)
    # ================================
    forecast_df = pd.DataFrame({
        "Mes": forecast.index,
        "Ventas Escenario Mínimo": lower.values,
        "Proyección Ventas (Base)": forecast.values,
        "Ventas Escenario Máximo": upper.values
    })

    for col in ["Ventas Escenario Mínimo", "Proyección Ventas (Base)", "Ventas Escenario Máximo"]:
        forecast_df[col] = forecast_df[col].round(0).astype("int64")

    os.makedirs("outputs", exist_ok=True)
    forecast_df.to_excel(output_forecast, index=False)

    print(f"✅ Reporte generado. RMSE Validación: {rmse_backtest:.4f} B")
    
    return forecast_df, lower, upper

