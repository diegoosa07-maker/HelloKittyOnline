import os
import pandas as pd
import sys

_SRC_DIR = os.path.dirname(os.path.dirname(__file__))
if _SRC_DIR not in sys.path:
    sys.path.insert(0, _SRC_DIR)

from models.incidencias import Incidencia, TIPOS, NIVELES_RIESGO
from utils.validators import validar_incidencia
from utils.io_utils import COLUMNAS, cargar_csv, guardar_csv, cargar_json, guardar_json

_DATA_DIR = os.path.join(_SRC_DIR, "..", "Data", "clean")
RUTA_CSV  = os.path.normpath(os.path.join(_DATA_DIR, "amenazas.csv"))
RUTA_JSON = os.path.normpath(os.path.join(_DATA_DIR, "amenazas.json"))


class IncidenciaController:

    def __init__(self, ruta_csv=RUTA_CSV, ruta_json=RUTA_JSON):
        self._ruta_csv  = ruta_csv
        self._ruta_json = ruta_json
        self._df = self._cargar_datos()

    def _cargar_datos(self):
        df = cargar_csv(self._ruta_csv)
        if not df.empty:
            return df
        return cargar_json(self._ruta_json)

    def _guardar(self):
        guardar_csv(self._df, self._ruta_csv)
        guardar_json(self._df, self._ruta_json)

    def recargar(self):
        self._df = self._cargar_datos()

    def registrar(self, nombre, clasificacion, nivel_riesgo):
        errores = validar_incidencia(nombre, clasificacion, TIPOS, nivel_riesgo, NIVELES_RIESGO)
        if errores:
            return errores

        incidencia = Incidencia(nombre=nombre, clasificacion=clasificacion, nivel_riesgo=nivel_riesgo)
        nueva_fila = pd.DataFrame([incidencia.to_dict()])
        self._df = pd.concat([self._df, nueva_fila], ignore_index=True)
        self._guardar()
        return []

    def eliminar(self, indice):
        if indice < 0 or indice >= len(self._df):
            return False
        self._df = self._df.drop(index=indice).reset_index(drop=True)
        self._guardar()
        return True

    def importar_csv(self, contenido_bytes):
        import io
        try:
            df_nuevo = pd.read_csv(io.BytesIO(contenido_bytes), encoding="utf-8")
            if not all(col in df_nuevo.columns for col in COLUMNAS):
                return False, f"El CSV no tiene las columnas requeridas: {COLUMNAS}"
            self._df = df_nuevo[COLUMNAS].dropna(how="all")
            self._guardar()
            return True, f"Se importaron {len(self._df)} incidencias correctamente."
        except Exception as e:
            return False, f"Error al importar CSV: {e}"

    def importar_json(self, contenido_bytes):
        import json
        try:
            datos = json.loads(contenido_bytes.decode("utf-8"))
            if not isinstance(datos, list):
                return False, "El JSON debe contener una lista de incidencias."
            df_nuevo = pd.DataFrame(datos)
            if not all(col in df_nuevo.columns for col in COLUMNAS):
                return False, f"El JSON no tiene las claves requeridas: {COLUMNAS}"
            self._df = df_nuevo[COLUMNAS].dropna(how="all")
            self._guardar()
            return True, f"Se importaron {len(self._df)} incidencias correctamente."
        except Exception as e:
            return False, f"Error al importar JSON: {e}"

    def obtener_df(self):
        return self._df.copy()

    def filtrar(self, clasificacion="Todos", nivel_riesgo="Todos"):
        df = self._df.copy()
        if clasificacion != "Todos":
            df = df[df["Clasificación"] == clasificacion]
        if nivel_riesgo != "Todos":
            df = df[df["Nivel de Riesgo"] == nivel_riesgo]
        return df

    def conteo_por_clasificacion(self):
        if self._df.empty:
            return pd.Series(dtype=int)
        return self._df["Clasificación"].value_counts()

    def conteo_por_nivel(self):
        if self._df.empty:
            return pd.Series(dtype=int)
        conteo = self._df["Nivel de Riesgo"].value_counts()
        return conteo.reindex([n for n in NIVELES_RIESGO if n in conteo.index])

    def evolucion_temporal(self):
        if self._df.empty:
            return pd.DataFrame(columns=["Fecha", "Total"])
        df = self._df.copy()
        df["_dia"] = pd.to_datetime(df["Fecha"], errors="coerce").dt.date
        return (
            df.groupby("_dia").size()
            .reset_index(name="Total")
            .rename(columns={"_dia": "Fecha"})
            .sort_values("Fecha")
        )

    def total_incidencias(self):
        return len(self._df)

    def nivel_mas_frecuente(self):
        if self._df.empty:
            return "-"
        return str(self._df["Nivel de Riesgo"].mode().iloc[0])

    def tipo_mas_frecuente(self):
        if self._df.empty:
            return "-"
        return str(self._df["Clasificación"].mode().iloc[0])
