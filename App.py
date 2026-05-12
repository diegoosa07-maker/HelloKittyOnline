import os
import sys

_SRC = os.path.dirname(os.path.abspath(__file__))
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

import streamlit as st



st.set_page_config(
    page_title="HelloKittyOnline — Gestión de Amenazas",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("HelloKittyOnline")
st.caption("Sistema de gestión y registro de amenazas cibernéticas")
st.divider()


if "controller" not in st.session_state:
    st.session_state.controller = IncidenciaController()

ctrl = st.session_state.controller

with st.sidebar:
    st.markdown("## Navegación")
    seccion = st.radio(
        "Ir a:",
        options=["Registrar amenaza", "Ver incidencias", "Estadísticas"],
        label_visibility="collapsed",
    )
    st.divider()
    st.caption(f"Total registradas: {ctrl.total_incidencias()} incidencias")

if seccion == "Registrar amenaza":
    render_registro(ctrl)
elif seccion == "Ver incidencias":
    render_tabla(ctrl)
elif seccion == "Estadísticas":
    render_estadisticas(ctrl)
