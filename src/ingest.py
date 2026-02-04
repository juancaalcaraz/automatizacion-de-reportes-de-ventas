#import pandas as pd
"""
def ingest_data(url: str) -> pd.DataFrame:
    df = pd.read_csv(url)
    df['indice_tiempo'] = pd.to_datetime(df['indice_tiempo'])
    return df.sort_values('indice_tiempo')
"""
import pandas as pd
import os

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
