import pandas as pd

def load_data(file_path):
    """
    Cargar datos desde un archivo CSV.
    """
    try:
        return pd.read_csv(file_path,encoding="utf-8")
    except FileNotFoundError:
        raise FileNotFoundError(f"Archivo no encontrado: {file_path}")
