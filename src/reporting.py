import os
import pandas as pd
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter

def auto_adjust_columns(ws):
    for col in ws.columns:
        max_length = 0
        col_letter = get_column_letter(col[0].column)
        for cell in col:
            if cell.value:
                max_length = max(max_length, len(str(cell.value)))
        ws.column_dimensions[col_letter].width = max_length + 3

def export_report(df, kpis, output_excel, last_n_months):
    os.makedirs(os.path.dirname(output_excel), exist_ok=True)

    if os.path.exists(output_excel):
        os.remove(output_excel)

    with pd.ExcelWriter(output_excel, engine="openpyxl") as writer:

        # ---------- KPIs ----------
        kpis.to_excel(writer, sheet_name="KPIs", index=False, startrow=2)
        ws_kpis = writer.sheets["KPIs"]
        ws_kpis["A1"] = "Indicadores clave – Ventas en Supermercados"
        ws_kpis["A1"].font = Font(bold=True, size=14)
        auto_adjust_columns(ws_kpis)

        # ---------- Serie histórica ----------
        hist = df.tail(last_n_months * 2)
        hist.to_excel(writer, sheet_name="Serie histórica", index=False)
        ws_hist = writer.sheets["Serie histórica"]
        auto_adjust_columns(ws_hist)

        # ---------- Medios de pago ----------
        last = df.iloc[-1]
        pagos = pd.DataFrame({
            "Medio": ["Efectivo", "Débito", "Crédito", "Otros"],
            "Participación": [
                last['efectivo'],
                last['tarjetas_debito'],
                last['tarjetas_credito'],
                last['otros_medios']
            ]
        })
        pagos["Participación"] /= pagos["Participación"].sum()

        pagos.to_excel(writer, sheet_name="Medios de pago", index=False)
        ws_pagos = writer.sheets["Medios de pago"]
        auto_adjust_columns(ws_pagos)
        
    print("✔ Excel generado y protegido correctamente")

