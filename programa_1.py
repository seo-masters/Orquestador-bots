import datetime

# Obtener la hora actual
hora_actual = datetime.datetime.now()

# Formatear la hora en un formato legible
hora_formateada = hora_actual.strftime("%H:%M:%S")

# Crear un mensaje que incluya la hora
mensaje = f"La hora de ejecución es: {hora_formateada}"

# Imprimir el mensaje
print(mensaje)