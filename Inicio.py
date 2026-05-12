import streamlit as st
import pandas as pd
import os
from datetime import datetime
import plotly.express as px

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="HelloKittyOnline - Gestión", 
    layout="wide", 
    initial_sidebar_state="auto"  # Ahora se comporta de forma normal
)

# Encabezado simple
st.title("HelloKittyOnline")
st.caption("Registro automatizado de amenazas cibernéticas")

# 2. CONFIGURACIÓN DE DATOS Y RUTAS
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.normpath(os.path.join(BASE_DIR, "data", "clean", "amenazas.csv"))
COLUMNAS = ["Amenaza", "Clasificación", "Nivel de Riesgo", "Acciones Recomendadas", "Fecha"]

INFO_AMENAZAS = {
    "Phishing": {"riesgo": "Medio", "accion": "No hacer clic en enlaces sospechosos..."},
    "Malware": {"riesgo": "Alto", "accion": "Aislar el sistema, ejecutar antivirus..."},
    "Ataque de fuerza bruta": {"riesgo": "Crítico", "accion": "Bloquear la cuenta, habilitar 2FA..."},
    "Fuga de datos": {"riesgo": "Crítico", "accion": "Identificar datos expuestos..."},
    "Acceso no autorizado": {"riesgo": "Alto", "accion": "Revocar credenciales..."},
    "Otros": {"riesgo": "Bajo", "accion": "Documentar el incidente..."},
}

# 3. LÓGICA DE CARGA/GUARDADO
def cargar():
    if os.path.exists(DATA_PATH):
        try:
            df = pd.read_csv(DATA_PATH)
            return df if list(df.columns) == COLUMNAS else pd.DataFrame(columns=COLUMNAS)
        except:
            return pd.DataFrame(columns=COLUMNAS)
    return pd.DataFrame(columns=COLUMNAS)

def guardar(df):
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    df.to_csv(DATA_PATH, index=False)

if "df" not in st.session_state:
    st.session_state.df = cargar()

# 4. INTERFAZ: REGISTRO DE AMENAZA
st.subheader("Registrar nueva amenaza")

opciones = ["Por favor seleccione:"] + list(INFO_AMENAZAS.keys())
clasif = st.selectbox("Tipo de amenaza", opciones)

if clasif != "Por favor seleccione:":
    nivel_auto = INFO_AMENAZAS[clasif]["riesgo"]
    accion_auto = INFO_AMENAZAS[clasif]["accion"]
    col_info1, col_info2 = st.columns([1, 3])
    with col_info1:
        st.info(f"*Riesgo:* {nivel_auto}")
    with col_info2:
        st.info(f"*Acción:* {accion_auto}")
else:
    nivel_auto = None
    accion_auto = None

with st.form("form_registro", clear_on_submit=True):
    nombre_amenaza = st.text_input("Nombre de la amenaza específica")
    boton_guardar = st.form_submit_button("Guardar en base de datos")

if boton_guardar:
    if clasif == "Por favor seleccione:":
        st.error("Debes seleccionar un tipo de amenaza.")
    elif not nombre_amenaza.strip():
        st.error("Por favor, introduce un nombre.")
    else:
        nueva_fila = {
            "Amenaza": nombre_amenaza, 
            "Clasificación": clasif,
            "Nivel de Riesgo": nivel_auto, 
            "Acciones Recomendadas": accion_auto,
            "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame([nueva_fila])], ignore_index=True)
        guardar(st.session_state.df)
        st.success(f"Registrado: {nombre_amenaza}")
        st.rerun()

st.divider()

# --- SECCIÓN: DASHBOARD Y GRÁFICAS ---
st.subheader(" Dashboard de Análisis")

if not st.session_state.df.empty:
    col_graf1, col_graf2 = st.columns(2)

    with col_graf1:
        st.markdown("### Amenazas por Clasificación")
        conteo_clasif = st.session_state.df['Clasificación'].value_counts()
        st.bar_chart(conteo_clasif, color="#ff4b4b")

    with col_graf2:
        st.markdown("### Niveles de Riesgo")
        conteo_riesgo = st.session_state.df['Nivel de Riesgo'].value_counts().reset_index()
        conteo_riesgo.columns = ['Riesgo', 'Cantidad']
        
        colores = {
            'Crítico': '#d32f2f', 
            'Alto': '#f57c00', 
            'Medio': '#fbc02d', 
            'Bajo': '#388e3c'
        }
        
        fig = px.pie(
            conteo_riesgo, 
            values='Cantidad', 
            names='Riesgo',
            hole=0.4,
            color='Riesgo',
            color_discrete_map=colores
        )
        st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Aún no hay datos suficientes para generar gráficas.")

st.divider()

# 5. TABLA DE RESULTADOS
st.subheader(" Historial de Registros")
if st.session_state.df.empty:
    st.info("No hay registros todavía.")
else:
    st.dataframe(st.session_state.df, use_container_width=True, hide_index=True)
    