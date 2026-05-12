import json
import os
import pandas as pd
from datetime import datetime

COLUMNAS = ["Amenaza", "Clasificación", "Nivel de Riesgo", "Acciones Recomendadas", "Fecha"]


def df_vacio():
    return pd.DataFrame(columns=COLUMNAS)


def cargar_csv(ruta):
    if not os.path.exists(ruta):
        return df_vacio()
    try:
        df = pd.read_csv(ruta, encoding="utf-8")
        if df.empty or not all(col in df.columns for col in COLUMNAS):
            return df_vacio()
        return df[COLUMNAS].dropna(how="all")
    except Exception as e:
        print(f"Error al cargar CSV: {e}")
        return df_vacio()


def guardar_csv(df, ruta):
    try:
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        df.to_csv(ruta, index=False, encoding="utf-8")
        return True
    except Exception as e:
        print(f"Error al guardar CSV: {e}")
        return False


def cargar_json(ruta):
    if not os.path.exists(ruta):
        return df_vacio()
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            datos = json.load(f)
        if not isinstance(datos, list) or len(datos) == 0:
            return df_vacio()
        df = pd.DataFrame(datos)
        if not all(col in df.columns for col in COLUMNAS):
            return df_vacio()
        return df[COLUMNAS].dropna(how="all")
    except Exception as e:
        print(f"Error al cargar JSON: {e}")
        return df_vacio()


def guardar_json(df, ruta):
    try:
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        registros = df.to_dict(orient="records")
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(registros, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Error al guardar JSON: {e}")
        return False


def df_a_csv_bytes(df):
    return df.to_csv(index=False).encode("utf-8")


def df_a_json_bytes(df):
    return json.dumps(df.to_dict(orient="records"), ensure_ascii=False, indent=2).encode("utf-8")


def generar_nombre_exportacion(extension):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"incidencias_{ts}.{extension}"
