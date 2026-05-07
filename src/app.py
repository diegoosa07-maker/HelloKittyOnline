import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="HelloKittyOnline")

st.title("HelloKittyOnline")
st.caption("Registro de amenazas cibernéticas")

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "Data", "clean", "amenazas.csv")
COLUMNAS  = ["Amenaza", "Clasificación", "Nivel de Riesgo", "Acciones Recomendadas", "Fecha"]

ACCIONES = {
    "Phishing":                "No hacer clic en enlaces sospechosos, reportar el correo y cambiar contraseñas afectadas.",
    "Malware":                 "Aislar el sistema, ejecutar antivirus actualizado y restaurar desde un backup limpio.",
    "Ataque de fuerza bruta":  "Bloquear la cuenta afectada, habilitar autenticación de dos factores y revisar logs de acceso.",
    "Fuga de datos":           "Identificar los datos expuestos, notificar a los afectados y revisar los controles de acceso.",
    "Acceso no autorizado":    "Revocar credenciales comprometidas, auditar permisos y reforzar la política de contraseñas.",
    "Otros":                   "Documentar el incidente y escalar al equipo de seguridad para su análisis.",
}

def cargar():
    if os.path.exists(DATA_PATH):
        try:
            df = pd.read_csv(DATA_PATH)
            if df.empty or list(df.columns) != COLUMNAS:
                return pd.DataFrame(columns=COLUMNAS)
            return df
        except Exception:
            return pd.DataFrame(columns=COLUMNAS)
    return pd.DataFrame(columns=COLUMNAS)

def guardar(df):
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    df.to_csv(DATA_PATH, index=False)

if "df" not in st.session_state:
    st.session_state.df = cargar()

# REGISTRO DE AMENAZA
st.subheader("Registrar amenaza")

clasif = st.selectbox("Tipo de amenaza", ["Por favor seleccione:"] + list(ACCIONES.keys()))

if clasif == "Por favor seleccione:":
    st.info("Al seleccionar el tipo de amenaza se mostrará en esta sección la recomendación adecuada.")
else:
    st.info(f"**Acción recomendada:** {ACCIONES[clasif]}")

with st.form("form", clear_on_submit=True):
    amenaza  = st.text_input("Nombre de la amenaza")
    nivel    = st.selectbox("Nivel de riesgo", ["Crítico", "Alto", "Medio", "Bajo"])
    guardar_ = st.form_submit_button("Guardar")

if guardar_:
    if clasif == "Por favor seleccione:":
        st.error("Selecciona un tipo de amenaza.")
    elif not amenaza.strip():
        st.error("Escribe el nombre de la amenaza.")
    else:
        nueva = {"Amenaza": amenaza, "Clasificación": clasif,
                 "Nivel de Riesgo": nivel, "Acciones Recomendadas": ACCIONES[clasif],
                 "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M")}
        st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame([nueva])], ignore_index=True)
        guardar(st.session_state.df)
        st.success(f"'{amenaza}' registrada correctamente.")
        st.rerun()

# AMENAZAS GUARDADAS (Tabla)
st.subheader("Amenazas registradas")

df = st.session_state.df
if df.empty:
    st.info("Aún no hay amenazas registradas.")
else:
    st.dataframe(df, width='stretch', hide_index=True)
