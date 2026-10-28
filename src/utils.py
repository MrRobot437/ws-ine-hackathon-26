import pandas as pd
import json

def num(n):
    """Cambia el formato de un número a miles con punto"""
    return f"{n:,}".replace(",", ".")

def pct(v):
    """Cambia el formato de un porcentaje a 1 decimal con coma"""
    return f"{v:.1f}".replace(".", ",") + "%"

def dec(v):
    """Cambia el formato de decimal con coma"""
    return f"{v:.1f}".replace(".", ",")

def convert_percentages(df):
    """Convierte las columnas en formato de texto a números en porcentaje (%)"""
    for col in df.columns:
        if df[col].dtype == "object" and df[col].astype(str).str.endswith("%").all():
            df[col] = (df[col].str.replace("%", "")
                              .str.replace(",", ".")
                              .astype(float))
    return df

def long_to_wide(df, index, medida="Nombres de medidas", valor="Valores de medidas"):
    """Convierte formato largo en formato ancho"""
    df = df.copy()
    df[medida] = df[medida].str.replace(r"^\d+\s+", "", regex=True).str.strip()   # "12   IMV" → "IMV"
    ancho = df.pivot_table(index=index, columns=medida, values=valor, aggfunc="first").reset_index()
    ancho.columns.name = None
    return ancho

def read_csv(ruta, sep=";", decimal=",", **kwargs):
    """Lee el archivo CSV y lo convierte en una tabla: DataFrame."""
    try:
        df = pd.read_csv(ruta, sep=sep, decimal=decimal, encoding="utf-8-sig", **kwargs)
    except UnicodeDecodeError:
        df = pd.read_csv(ruta, sep=sep, decimal=decimal, encoding="latin-1", **kwargs)

    df.columns = df.columns.str.strip()   # eliminar el espacio en los encabezados
    return df

def convert_geojson_to_structure(ruta):
    """Convertir GeoJSON a diccionario en Python"""
    with open(ruta, encoding="utf-8") as f:
        geojson = json.load(f)
    return geojson
