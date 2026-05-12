from datetime import datetime

NIVELES_RIESGO = ["Crítico", "Alto", "Medio", "Bajo"]

TIPOS = [
    "Phishing",
    "Malware",
    "Ataque de fuerza bruta",
    "Fuga de datos",
    "Acceso no autorizado",
    "Otros",
]

ACCIONES = {
    "Phishing": "No hacer clic en enlaces sospechosos, reportar el correo y cambiar contraseñas afectadas.",
    "Malware": "Aislar el sistema, ejecutar antivirus actualizado y restaurar desde un backup limpio.",
    "Ataque de fuerza bruta": "Bloquear la cuenta afectada, habilitar autenticación de dos factores y revisar logs de acceso.",
    "Fuga de datos": "Identificar los datos expuestos, notificar a los afectados y revisar los controles de acceso.",
    "Acceso no autorizado": "Revocar credenciales comprometidas, auditar permisos y reforzar la política de contraseñas.",
    "Otros": "Documentar el incidente y escalar al equipo de seguridad para su análisis.",
}


class Incidencia:
    def __init__(self, nombre, clasificacion, nivel_riesgo, fecha=None):
        self.nombre = nombre.strip()
        self.clasificacion = clasificacion
        self.nivel_riesgo = nivel_riesgo
        self.fecha = fecha or datetime.now().strftime("%Y-%m-%d %H:%M")

    def accion_recomendada(self):
        return ACCIONES.get(self.clasificacion, "Documentar y escalar al equipo de seguridad.")

    def to_dict(self):
        return {
            "Amenaza": self.nombre,
            "Clasificación": self.clasificacion,
            "Nivel de Riesgo": self.nivel_riesgo,
            "Acciones Recomendadas": self.accion_recomendada(),
            "Fecha": self.fecha,
        }
