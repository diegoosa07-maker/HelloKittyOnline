def validar_incidencia(nombre, clasificacion, tipos_validos, nivel_riesgo, niveles_validos):
    errores = []

    nombre = nombre.strip()
    if not nombre:
        errores.append("El nombre no puede estar vacío.")
    elif len(nombre) < 3:
        errores.append("El nombre debe tener al menos 3 caracteres.")
    elif len(nombre) > 100:
        errores.append("El nombre no puede superar 100 caracteres.")
    elif nombre.isdigit():
        errores.append("El nombre no puede ser solo números.")

    if clasificacion not in tipos_validos:
        errores.append("Debes seleccionar un tipo de amenaza válido.")

    if nivel_riesgo not in niveles_validos:
        errores.append("Debes seleccionar un nivel de riesgo válido.")

    return errores
