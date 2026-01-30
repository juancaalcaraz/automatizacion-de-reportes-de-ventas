
### Configuración de la ingesta de dato.
#DATA_URL = "https://infra.datos.gob.ar/catalog/sspm/dataset/455/distribution/455.1/download/ventas-totales-supermercados-2.csv"
DATA_URL = "ventas-totales-supermercados-2.csv"
OUTPUT_EXCEL = "outputs/report.xlsx"
OUTPUT_FORECAST = "outputs/forecast_escenarios.xlsx"
FIGURES_DIR = "outputs/figures"

LAST_N_MONTHS = 12

########################################
#  Configuraación de envio de E-mails. #
########################################

SEND_EMAIL = False  # <- cambiar a True cuando quieras enviar
EMAIL_RECIPIENTS = ["cliente@empresa.com"]

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "tu_email@gmail.com"
SMTP_PASSWORD = "APP_PASSWORD_AQUI"  #  usar app password
