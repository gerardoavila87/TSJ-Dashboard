import pandas as pd

def load_data(file_path):
    data = process_data(file_path)
    return data
    
def process_data(file_path):
    try:
        return pd.read_csv(file_path,encoding="utf-8")
    except FileNotFoundError:
        raise FileNotFoundError(f"Archivo no encontrado: {file_path}")