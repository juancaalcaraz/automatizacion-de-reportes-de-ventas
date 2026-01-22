import os
import smtplib
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
    if not send_email:
        print("📭 Envío de emails desactivado para esta ejecución.")
        return

    if not recipients:
        raise ValueError("Se indicó enviar email pero no hay destinatarios.")

    print("📤 Enviando reporte por email...")

    msg = EmailMessage()
    msg["From"] = smtp_user
    msg["To"] = ", ".join(recipients)
    msg["Subject"] = subject
    msg.set_content(body)

    # Adjuntos
    for path in attachments:
        if not os.path.exists(path):
            raise FileNotFoundError(f"No existe el archivo adjunto: {path}")

        with open(path, "rb") as f:
            file_data = f.read()

        filename = os.path.basename(path)
        msg.add_attachment(
            file_data,
            maintype="application",
            subtype="octet-stream",
            filename=filename
        )

    # Envío
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)

    print("✅ Email enviado correctamente.")
