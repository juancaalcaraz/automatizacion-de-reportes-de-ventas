import pandas as pd

def ingest_data(url: str) -> pd.DataFrame:
    df = pd.read_csv(url)
    df['indice_tiempo'] = pd.to_datetime(df['indice_tiempo'])
    return df.sort_values('indice_tiempo')
