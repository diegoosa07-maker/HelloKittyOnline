import streamlit as st
import pandas as pd
import plotly.express as px

import os
from datetime import datetime

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="HelloKittyOnline — Gestión", layout="wide")

# Archivo donde se guardará la información
ARCHIVO_DATOS = "amenazas.csv"

# Opciones fijas para los selectores
NIVELES_RIESGO = ["Crítico", "Alto", "Medio", "Bajo"]
TIPOS_AMENAZA = ["Phishing", "Malware", "Ataque de fuerza bruta", "Fuga de datos", "Acceso no autorizado", "Otros"]

# Diccionario de acciones recomendadas
ACCIONES = {
    "Phishing": "No hacer clic en enlaces sospechosos y reportar el correo.",
    "Malware": "Aislar el sistema y ejecutar un antivirus actualizado.",
    "Ataque de fuerza bruta": "Bloquear la cuenta y habilitar autenticación de dos factores.",
    "Fuga de datos": "Identificar datos expuestos y notificar a los afectados.",
    "Acceso no autorizado": "Revocar credenciales y auditar permisos de usuario.",
    "Otros": "Documentar el incidente y escalar al equipo de seguridad."
}

# 2. FUNCIONES DE APOYO (Lógica de datos)
def cargar_datos():
    """Carga el CSV si existe, si no, crea un DataFrame vacío."""
    if os.path.exists(ARCHIVO_DATOS):
        return pd.read_csv(ARCHIVO_DATOS)
    return pd.DataFrame(columns=["Amenaza", "Clasificación", "Nivel de Riesgo", "Acción", "Fecha"])

def guardar_datos(df):
    """Guarda el DataFrame actual en el archivo CSV."""
    df.to_csv(ARCHIVO_DATOS, index=False)

# Inicializamos los datos en