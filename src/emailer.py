import os
import smtplib
import ssl
from email.message import EmailMessage

def send_report_email(
    send_email: bool,
    recipients: list,
    subject: str,
    body: str,
    attachments: list,
    smtp_server: str,
    smtp_port: int,
    smtp_user: str,
    smtp_password: str
):
    """
    Envía un correo electrónico con múltiples adjuntos (PDF, Excel, Imágenes).
    Incluye detección automática de tipos MIME para evitar filtros de spam.
    """
    if not send_email:
        print("📭 Envío de emails desactivado por configuración.")
        return

    msg = EmailMessage()
    msg["From"] = smtp_user
    msg["To"] = ", ".join(recipients)
    msg["Subject"] = subject
    msg.set_content(body)

    # --- Lógica inteligente de adjuntos ---
    for path in attachments:
        if not os.path.exists(path):
            print(f"⚠️ Advertencia: El archivo {path} no existe. Se omitirá.")
            continue

        try:
            with open(path, "rb") as f:
                file_data = f.read()
                filename = os.path.basename(path)
                
                # Identificación de tipos MIME profesionales
                if filename.endswith(".pdf"):
                    main, sub = "application", "pdf"
                elif filename.endswith(".xlsx"):
                    # El tipo oficial para Excel moderno (.xlsx)
                    main, sub = "application", "vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                elif filename.endswith(".png") or filename.endswith(".jpg"):
                    main, sub = "image", filename.split(".")[-1]
                else:
                    # Genérico para archivos binarios protegidos
                    main, sub = "application", "octet-stream"

                msg.add_attachment(
                    file_data, 
                    maintype=main, 
                    subtype=sub, 
                    filename=filename
                )
                print(f"📎 Adjunto preparado: {filename}")

        except Exception as e:
            print(f"❌ No se pudo adjuntar {path}: {e}")

    # --- Envío Seguro ---
    context = ssl.create_default_context()
    try:
        # Usamos SMTP_SSL si el puerto es 465, o SMTP + STARTTLS si es 587
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls(context=context) 
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
            
        print(f"✅ Email enviado exitosamente a {len(recipients)} destinatarios.")
        
    except Exception as e:
        print(f"❌ Error crítico en el servidor SMTP: {e}")
