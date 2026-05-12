import streamlit as st
import pandas as pd
import os
from datetime import datetime

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="HelloKittyOnline - Gestión", layout="wide")

# Encabezado con botón lateral
col_titulo, col_boton = st.columns([4, 1])

with col_titulo:
    st.title("HelloKittyOnline")
    st.caption("Registro automatizado de amenazas cibernéticas")

with col_boton:
    if st.button("👥 Sobre Nosotros"):
        # Esta forma es la más robusta:
        st.switch_page(os.path.join("pages", "Sobre_Nosotros.py"))
    if st.button("📖 Ver Definiciones"):
        st.switch_page("pages/Definiciones_Amenazas.py")

# 2. CONFIGURACIÓN DE DATOS Y RUTAS
# Ajustamos la ruta para que siempre encuentre los datos sin importar dónde se ejecute
_BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.normpath(os.path.join(_BASE_DIR, "data", "clean", "amenazas.csv"))
COLUMNAS = ["Amenaza", "Clasificación", "Nivel de Riesgo", "Acciones Recomendadas", "Fecha"]

# Diccionario ampliado con Recomendación Y Nivel de Riesgo sugerido
INFO_AMENAZAS = {
    "Phishing": {
        "riesgo": "Medio",
        "accion": "No hacer clic en enlaces sospechosos, reportar el correo y cambiar contraseñas."
    },
    "Malware": {
        "riesgo": "Alto",
        "accion": "Aislar el sistema, ejecutar antivirus y restaurar desde backup limpio."
    },
    "Ataque de fuerza bruta": {
        "riesgo": "Crítico",
        "accion": "Bloquear la cuenta, habilitar 2FA y revisar logs de acceso."
    },
    "Fuga de datos": {
        "riesgo": "Crítico",
        "accion": "Identificar datos expuestos, notificar afectados y revisar controles."
    },
    "Acceso no autorizado": {
        "riesgo": "Alto",
        "accion": "Revocar credenciales, auditar permisos y reforzar contraseñas."
    },
    "Otros": {
        "riesgo": "Bajo",
        "accion": "Documentar el incidente y escalar al equipo de seguridad."
    },
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

# Selector de tipo de amenaza
opciones = ["Por favor seleccione:"] + list(INFO_AMENAZAS.keys())
clasif = st.selectbox("Tipo de amenaza", opciones)

# Lógica automática de nivel y recomendación
if clasif != "Por favor seleccione:":
    nivel_auto = INFO_AMENAZAS[clasif]["riesgo"]
    accion_auto = INFO_AMENAZAS[clasif]["accion"]
    
    # Mostramos la información que se asignará automáticamente
    col_info1, col_info2 = st.columns([1, 3])
    with col_info1:
        st.info(f"**Riesgo asignado:** {nivel_auto}")
    with col_info2:
        st.info(f"**Acción recomendada:** {accion_auto}")
else:
    nivel_auto = None
    accion_auto = None
    st.info("Selecciona un tipo para ver la clasificación automática.")

# Formulario (ahora más corto ya que el nivel es automático)
with st.form("form_registro", clear_on_submit=True):
    nombre_amenaza = st.text_input("Nombre de la amenaza específica")
    boton_guardar = st.form_submit_button("Guardar en base de datos")

if boton_guardar:
    if clasif == "Por favor seleccione:":
        st.error("Debes seleccionar un tipo de amenaza.")
    elif not nombre_amenaza.strip():
        st.error("Por favor, introduce un nombre para la amenaza.")
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
        st.success(f"Registrado: {nombre_amenaza} (Nivel {nivel_auto})")
        st.rerun()

st.divider()

# 5. TABLA DE RESULTADOS
st.subheader("Amenazas registradas")
if st.session_state.df.empty:
    st.info("No hay registros todavía.")
else:
    st.dataframe(st.session_state.df, use_container_width=True, hide_index=True)