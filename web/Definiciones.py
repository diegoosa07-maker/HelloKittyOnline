import streamlit as st
import io

st.set_page_config(page_title="Gestor de Amenazas Informáticas", layout="centered")
st.title("Gestor de Amenazas Informáticas")

if 'amenazas' not in st.session_state:
    st.session_state['amenazas'] = [
        {
            "nombre": "Malware",
            "definicion": "Software malicioso diseñado para dañar, explotar o acceder sin autorización a sistemas informáticos.",
            "apps": ["Malwarebytes", "Windows Defender"]
        },
        {
            "nombre": "Phishing",
            "definicion": "Técnica de engaño para obtener información confidencial haciéndose pasar por una entidad confiable.",
            "apps": ["Norton", "Kaspersky"]
        },
        {
            "nombre": "DDoS",
            "definicion": "Ataque de denegación de servicio distribuido que satura un sistema con tráfico para hacerlo inaccesible.",
            "apps": ["Cloudflare", "Incapsula"]
        },
        {
            "nombre": "Ransomware",
            "definicion": "Malware que cifra archivos y exige un rescate para restaurar el acceso.",
            "apps": ["Bitdefender", "Emsisoft Decryptor"]
        },
        {
            "nombre": "Spyware",
            "definicion": "Software que recopila información sobre un usuario sin su conocimiento.",
            "apps": ["SUPERAntiSpyware", "Spybot"]
        }
    ]



if st.session_state['amenazas']:
    opciones = [a['nombre'] for a in st.session_state['amenazas']]
    seleccion = st.selectbox("Selecciona una amenaza para ver detalles", opciones)
    amenaza = next((a for a in st.session_state['amenazas'] if a['nombre'] == seleccion), None)
    if amenaza:
        st.subheader(amenaza['nombre'])
        st.text_area("Definición y detalles", amenaza['definicion'], height=120, disabled=True)
        if amenaza['apps']:
            st.write("**Apps recomendadas:**")
            for app in amenaza['apps']:
                st.write(f"- {app}")
        else:
            st.write("No se ingresaron apps recomendadas.")
else:
    st.info("No hay amenazas ingresadas.")


# Elimina la sección de definiciones abajo. Muestra la definición y apps solo al seleccionar del dropdown arriba.
