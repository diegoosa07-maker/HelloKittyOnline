import streamlit as st
from controllers.incidencia_controller import IncidenciaController
from models.incidencias import TIPOS, NIVELES_RIESGO, ACCIONES

PLACEHOLDER_TIPO = "— Selecciona un tipo —"


def render_registro(ctrl):
    st.subheader("Registrar nueva incidencia")

    # Selector de tipo de amenaza
    clasif = st.selectbox(
        "Tipo de amenaza",
        options=[PLACEHOLDER_TIPO] + TIPOS,
        key="sel_clasificacion",
    )

    if clasif == PLACEHOLDER_TIPO:
        st.info("Selecciona el tipo de amenaza para ver la acción recomendada.")
    else:
        st.success(f"**Acción recomendada:** {ACCIONES[clasif]}")

    st.divider()

    # Formulario de registro
    with st.form("form_registro", clear_on_submit=True):
        nombre = st.text_input(
            "Nombre de la amenaza",
            placeholder="Ej: Correo suplantando a BBVA",
        )
        nivel = st.selectbox("Nivel de riesgo", options=NIVELES_RIESGO)
        enviado = st.form_submit_button("Guardar incidencia", type="primary")

    if enviado:
        if clasif == PLACEHOLDER_TIPO:
            st.error("Debes seleccionar un tipo de amenaza antes de guardar.")
            return

        errores = ctrl.registrar(nombre=nombre, clasificacion=clasif, nivel_riesgo=nivel)

        if errores:
            for err in errores:
                st.error(err)
        else:
            st.success(f"Incidencia '{nombre.strip()}' registrada correctamente.")
            st.session_state.df = ctrl.obtener_df()
            st.rerun()
