from config import DATA_URL, OUTPUT_EXCEL, FIGURES_DIR, LAST_N_MONTHS, OUTPUT_FORECAST

from src.ingest import ingest_data
from src.validation import validate_data
from src.metrics import compute_kpis
from src.visualization import plot_sales
from src.forecast import plot_forecast_holt_winters
from src.reporting import export_report
from src.pdf_report import generate_pdf
from src.security import protect_pdf, protect_excel
from src.emailer import send_report_email
import os
from dotenv import load_dotenv
# === Cargar variables de entorno ===
load_dotenv()
PASSWORD = os.getenv("PASSWORD")
# Extraemos las variables del envio del mail en .env
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASS")
# destinatarios de los e-mails. 
EMAIL_RECIPIENTS = os.getenv("EMAIL_RECIPIENTS").split(",")
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
    protect_excel(OUTPUT_FORECAST,PASSWORD, blind=True)
    print("Exportando reporte...")
    export_report(df, kpis, OUTPUT_EXCEL, LAST_N_MONTHS)

    print("Reporte generado correctamente.")

    print("Encriptando Reporte en Excel")
    protect_excel(OUTPUT_EXCEL, PASSWORD)
    print("Generando PDF ejecutivo...")
    generate_pdf(kpis, forecast_data, FIGURES_DIR, PDF_PATH)
    print("Encriptando PDF...")
    protect_pdf(PDF_PATH, PASSWORD)
    print("Proceso de envío de email...")
    send_report_email(
    send_email=False,
    recipients=EMAIL_RECIPIENTS,
    subject=os.getenv("EMAIL_SUBJECT"),
    body=(
        "Adjuntamos el reporte mensual actualizado.\n\n"
        "Este informe fue generado automáticamente.\n\n"
        "Saludos."
    ),
    attachments=[EXCEL_PATH, PDF_PATH, OUTPUT_FORECAST],
    smtp_server=os.getenv("SMTP_SERVER"),
    smtp_port=int(os.getenv("SMTP_PORT")),
    smtp_user=SMTP_USER,
    smtp_password=SMTP_PASSWORD
    ) 
if __name__ == "__main__":
    main()
