import pandas as pd

def compute_kpis(df: pd.DataFrame) -> pd.DataFrame:
    last = df.iloc[-1]
    prev_year = df.iloc[-13]

    return pd.DataFrame([{
        "Fecha": last['indice_tiempo'],
        "Ventas reales último mes": last['ventas_precios_constantes'],
        "Variación interanual (%)":
            (last['ventas_precios_constantes'] /
             prev_year['ventas_precios_constantes'] - 1) * 100,
        "Participación canal online (%)":
            last['canales_on_line'] /
            last['ventas_totales_canal_venta'] * 100
    }])
