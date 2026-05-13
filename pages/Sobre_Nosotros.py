import streamlit as st

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Sobre Nosotros", layout="wide")

# 2. BOTÓN DE REGRESO
if st.button("Volver al Panel"):
    st.switch_page("App.py")

# 3. SOBRE NOSOTROS
st.title("Sobre Nosotros")

# 3. DATOS
EQUIPO = [
    {"nombre": "Rodrigo", "rol": "Programador"},
    {"nombre": "Carlos",  "rol": "Programador"},
    {"nombre": "Diego",   "rol": "Programador"},
    {"nombre": "Felipe",  "rol": "Programador"},
    {"nombre": "Adrian",  "rol": "Programador"},
]

PROFESORA = {
    "nombre": "Vanessa Lara Perez",
    "rol":    "Profesora del curso",
}


st.caption("Conoce al equipo detrás de HelloKittyOnline")
st.divider()

st.subheader("Equipo de desarrollo")

cols = st.columns(len(EQUIPO))
for col, miembro in zip(cols, EQUIPO):
    with col:
        st.markdown(f"### {miembro['nombre']}")
        st.caption(miembro["rol"])

st.divider()

st.subheader("Profesora")
st.markdown(f"**{PROFESORA['nombre']}**")
st.caption(PROFESORA["rol"])
