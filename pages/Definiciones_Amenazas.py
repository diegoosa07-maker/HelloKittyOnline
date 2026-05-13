
import streamlit as st
import io

# 1. DEFINICION DE LA PAGINA
st.set_page_config(page_title="Gestor de Amenazas Informáticas", layout="centered")

# 2. BOTÓN DE RETORNO 
if st.button("Volver al Panel"):
    st.switch_page("App.py")

st.title("Gestor de Amenazas Informáticas")

# Clase para representar una amenaza
class Amenaza:
    def __init__(self, nombre, definicion, apps=None):
        self.nombre = nombre
        self.definicion = definicion
        self.apps = apps if apps is not None else []

# Clase para gestionar las amenazas
class GestorAmenazas:
    def __init__(self, amenazas=None):
        if amenazas is None:
            amenazas = []
        self.amenazas = amenazas

    def obtener_nombres(self):
        return [a.nombre for a in self.amenazas]

    def obtener_por_nombre(self, nombre):
        return next((a for a in self.amenazas if a.nombre == nombre), None)

# Inicializar amenazas si no existen
if 'gestor_amenazas' not in st.session_state:
    amenazas_iniciales = [
        Amenaza("Malware", "Software malicioso diseñado para dañar, explotar o acceder sin autorización.", ["Malwarebytes", "Windows Defender"]),
        Amenaza("Phishing", "Técnica de engaño para obtener información confidencial haciéndose pasar por una entidad confiable.", ["Norton", "Kaspersky"]),
        Amenaza("DDoS", "Ataque que satura un sistema con tráfico para hacerlo inaccesible.", ["Cloudflare", "Incapsula"]),
        Amenaza("Ransomware", "Malware que cifra archivos y exige un rescate para restaurar el acceso.", ["Bitdefender", "Emsisoft Decryptor"]),
        Amenaza("Spyware", "Software que recopila información sobre un usuario sin su conocimiento.", ["SUPERAntiSpyware", "Spybot"]),
        # NUEVAS AÑADIDAS:
        Amenaza("Ataque de fuerza bruta", "Intento de adivinar contraseñas mediante prueba y error sistemático.", ["Authy", "Google Authenticator"]),
        Amenaza("Fuga de datos", "Liberación no autorizada de información confidencial hacia un entorno no confiable.", ["Varonis", "Digital Guardian"]),
        Amenaza("Acceso no autorizado", "Entrada a sistemas o redes sin el permiso debido.", ["Okta", "Cisco Duo"]),
        Amenaza("Otros", "Otras amenazas no categorizadas en las secciones anteriores.", ["Guía de Incidencias"])
    ]
    st.session_state['gestor_amenazas'] = GestorAmenazas(amenazas_iniciales)

gestor = st.session_state['gestor_amenazas']

if gestor.amenazas:
    opciones = gestor.obtener_nombres()
    seleccion = st.selectbox("Selecciona una amenaza para ver detalles", opciones)
    amenaza = gestor.obtener_por_nombre(seleccion)
    if amenaza:
        st.subheader(amenaza.nombre)
        st.text_area("Definición y detalles", amenaza.definicion, height=120, disabled=True)
        if amenaza.apps:
            st.write("**Apps recomendadas:**")
            for app in amenaza.apps:
                st.write(f"- {app}")
        else:
            st.write("No se ingresaron apps recomendadas.")
else:
    st.info("No hay amenazas ingresadas.")
