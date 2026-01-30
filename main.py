from config import DATA_URL, OUTPUT_EXCEL, FIGURES_DIR, LAST_N_MONTHS, OUTPUT_FORECAST

from src.ingest import ingest_data
from src.validation import validate_data
from src.metrics import compute_kpis
from src.visualization import plot_sales
from src.forecast import  plot_forecast_holt_winters
from src.reporting import export_report
from src.pdf_report import generate_pdf
from src.security import  protect_pdf, protect_excel
from config import (
    SEND_EMAIL,
    EMAIL_RECIPIENTS,
    SMTP_SERVER,
    SMTP_PORT,
    SMTP_USER,
    SMTP_PASSWORD
)

from src.emailer import send_report_email

PDF_PATH = "outputs/reporte_ejecutivo.pdf"
EXCEL_PATH = OUTPUT_EXCEL
def main():
    print("Ingestando datos...")
    df = ingest_data(DATA_URL)

    print("Validando datos...")
    validate_data(df)

    print("Calculando KPIs...")
    kpis = compute_kpis(df)

    print("Generando gráficos...")
    plot_sales(df, FIGURES_DIR)
    
    print("Generando pronóstico...")
    forecast_data, lower, upper = plot_forecast_holt_winters(
        df,
        FIGURES_DIR,OUTPUT_FORECAST, 
        horizon=3
    )
    print("Cifrando el Forecast...")
    protect_excel(OUTPUT_FORECAST,"4ut0m4t1zac1*n")
    print("Exportando reporte...")
    export_report(df, kpis, OUTPUT_EXCEL, LAST_N_MONTHS)

    print("Reporte generado correctamente.")

    print("Encriptando Reporte en Excel")
    protect_excel(OUTPUT_EXCEL, "4ut0m4t1zac1*n")
    print("Generando PDF ejecutivo...")
    generate_pdf(kpis, forecast_data, FIGURES_DIR, PDF_PATH)
    print("Encriptando PDF...")
    protect_pdf(PDF_PATH, "4ut0m4t1zac1*n")
    print("Proceso de envío de email...")
    send_report_email(
    send_email=SEND_EMAIL,
    recipients=EMAIL_RECIPIENTS,
    subject="Reporte mensual – Ventas en Supermercados",
    body=(
        "Adjuntamos el reporte mensual actualizado.\n\n"
        "Este informe fue generado automáticamente.\n\n"
        "Saludos."
    ),
    attachments=[EXCEL_PATH, PDF_PATH],
    smtp_server=SMTP_SERVER,
    smtp_port=SMTP_PORT,
    smtp_user=SMTP_USER,
    smtp_password=SMTP_PASSWORD
    )
if __name__ == "__main__":
    main()
