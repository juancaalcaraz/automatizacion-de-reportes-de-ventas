import PyPDF2
import msoffcrypto
import io
import os

def protect_pdf(input_path, password):
    """
    Cifra un archivo PDF existente mediante una contraseña.
    
    Args:
        input_path (str): Ruta local del archivo PDF a proteger.
        password (str): Contraseña que se aplicará al archivo.
    """
    try:
        if not os.path.exists(input_path):
            print(f"⚠️ Error: No se encontró el PDF en {input_path}")
            return

        reader = PyPDF2.PdfReader(input_path)
        writer = PyPDF2.PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        writer.encrypt(user_password="1234", owner_password=password, permissions_flag=-3904)

        with open(input_path, "wb") as f:
            writer.write(f)
        
        print(f"🔒 PDF encriptado correctamente: {os.path.basename(input_path)}")
        
    except Exception as e:
        print(f"❌ Error al encriptar el PDF: {e}")

def protect_excel(file_path, password):
    """
    Cifra un archivo Excel (.xlsx) mediante el estándar de Microsoft Office.
    
    Args:
        file_path (str): Ruta local del archivo Excel a proteger.
        password (str): Contraseña que se aplicará al archivo.
    """
    try:
        if not os.path.exists(file_path):
            print(f"⚠️ Error: No se encontró el Excel en {file_path}")
            return

        # Leer el archivo original en binario
        with open(file_path, "rb") as f:
            file_data = io.BytesIO(f.read())

        encrypted = io.BytesIO()
        ms_file = msoffcrypto.OfficeFile(file_data)
        
        # Aplicar encriptación
        ms_file.encrypt(password, encrypted)

        # Sobrescribir el archivo original con los datos encriptados
        with open(file_path, "wb") as f:
            f.write(encrypted.getbuffer())
        
        print(f"🔒 Excel encriptado correctamente: {os.path.basename(file_path)}")
        
    except Exception as e:
        print(f"❌ Error al encriptar el Excel: {e}")
