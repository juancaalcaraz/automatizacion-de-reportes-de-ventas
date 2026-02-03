import PyPDF2
import msoffcrypto
import io
import os
import secrets
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter

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

def protect_sheet_only(file_path, password="", blind=False):
    wb = load_workbook(file_path)
    target_password = secrets.token_hex(16) if blind else password
    
    for ws in wb.worksheets:
        # 1. AUTOAJUSTE: Iterar por columnas antes de proteger
        for column in ws.columns:
            max_length = 0
            column_letter = column[0].column_letter # Obtiene la letra (A, B, C...)
            
            for cell in column:
                try:
                    if cell.value:
                        # Calculamos el largo del texto en la celda
                        val_len = len(str(cell.value))
                        if val_len > max_length:
                            max_length = val_len
                except:
                    pass
            
            # Ajustar ancho con un margen extra (factor de 1.2 o +2 caracteres)
            adjusted_width = (max_length + 2)
            ws.column_dimensions[column_letter].width = adjusted_width

        # 2. PROTECCIÓN: Ahora que el diseño es correcto, bloqueamos
        ws.protection.sheet = True
        ws.protection.password = target_password
        
    wb.save(file_path)



def protect_excel(file_path, password, protect_sheet=True , blind=False):
    """
    Cifra un archivo Excel (.xlsx) mediante el estándar de Microsoft Office.
    
    Args:
        file_path (str): Ruta local del archivo Excel a proteger.
        password (str): Contraseña que se aplicará al archivo.
    """
    if protect_sheet:
        if blind:
            protect_sheet_only(file_path, blind=True)
        else:
            protect_sheet_only(file_path, password)
            
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
