import pandas as pd
import os
import shutil
from datetime import datetime

def ingest_data(url: str, name: str="ventas-totales-supermercados-2") -> pd.DataFrame:
    """
    Gestiona la ingesta de datos: descarga si no existe localmente,
    guarda una copia y retorna un DataFrame procesado.
    """
    # 1. Definir la ruta del directorio y del archivo
    directory = "data/ingest"
    file_path = os.path.join(directory, f"{name}.csv")
    
    # 2. Verificar si el archivo ya existe localmente
    if os.path.exists(file_path):
        print(f"Cargando datos locales desde: {file_path}")
        df = pd.read_csv(file_path)
    else:
        print(f"Descargando datos desde la URL...")
        # Crear el directorio si no existe
        os.makedirs(directory, exist_ok=True)
        
        # Descargar y guardar el archivo
        df = pd.read_csv(url)
        df.to_csv(file_path, index=False)
        print(f"Archivo guardado exitosamente en: {file_path}")

    # 3. Procesamiento común (independiente de si fue local o descarga)
    df['indice_tiempo'] = pd.to_datetime(df['indice_tiempo'])
    return df.sort_values('indice_tiempo')

def archive_sent_files(file_list: list):
    """
    Crea una carpeta con la marca de tiempo en data/sended 
    y mueve los archivos enviados a dicha carpeta.
    """
    # 1. Crear el nombre de la carpeta con fecha y hora (ej: 2023-10-27_14-30-05)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    target_directory = os.path.join("data", "sended", timestamp)
    
    try:
        # 2. Crear la carpeta de destino
        os.makedirs(target_directory, exist_ok=True)
        
        # 3. Mover cada archivo de la lista
        for file_path in file_list:
            if os.path.exists(file_path):
                # Extraemos solo el nombre del archivo para la ruta de destino
                file_name = os.path.basename(file_path)
                dest_path = os.path.join(target_directory, file_name)
                
                shutil.move(file_path, dest_path)
                print(f"Archivo archivado: {file_name} -> {target_directory}")
            else:
                print(f"Advertencia: El archivo {file_path} no existe y no se pudo mover.")
                
        return target_directory

    except Exception as e:
        print(f"Error al archivar los archivos: {e}")
        return None

