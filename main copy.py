# import tkinter as tk
# from tkinter import ttk

# def mostrar_seleccion():
#     seleccion_dia = combo_dias.get()
#     seleccionados = [dia.get() for dia in dias_seleccionados]
#     mensaje = f"Día seleccionado: {seleccion_dia}\nDías de la semana seleccionados: {', '.join(seleccionados)}"
#     label_resultado.config(text=mensaje)

# # Crear la ventana principal
# ventana = tk.Tk()
# ventana.title("Selector de Días de la Semana")

# # ComboBox para seleccionar un día de la semana
# etiqueta_combo = ttk.Label(ventana, text="Selecciona un día de la semana:")
# etiqueta_combo.pack()
# dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
# combo_dias = ttk.Combobox(ventana, values=dias_semana)
# combo_dias.pack()

# # Botones para seleccionar varios días de la semana
# etiqueta_botones = ttk.Label(ventana, text="Selecciona uno o más días de la semana:")
# etiqueta_botones.pack()
# dias_seleccionados = []
# for dia in dias_semana:
#     dia_var = tk.StringVar()
#     check_button = ttk.Checkbutton(ventana, text=dia, variable=dia_var, onvalue=dia, offvalue="")
#     dia_var.set("")
#     check_button.pack()
#     dias_seleccionados.append(dia_var)

# # Botón para mostrar la selección
# boton_mostrar = ttk.Button(ventana, text="Mostrar Selección", command=mostrar_seleccion)
# boton_mostrar.pack()

# # Etiqueta para mostrar el resultado
# label_resultado = ttk.Label(ventana, text="")
# label_resultado.pack()

# ventana.mainloop()

# -------------------------------------------------------------------------------------------------------------------------------- Ejecucion de archivos .exe

# import tkinter as tk
# from tkinter import filedialog
# import os

# def listar_elementos_carpeta():
#     # Obtener la carpeta seleccionada por el usuario
#     carpeta_seleccionada = filedialog.askdirectory()

#     if carpeta_seleccionada:
#         # Listar elementos en la carpeta
#         elementos = os.listdir(carpeta_seleccionada)

#         # Mostrar las rutas de los elementos
#         for elemento in elementos:
#             ruta_elemento = os.path.join(carpeta_seleccionada, elemento)
            
#             # Verificar si el elemento es un archivo .exe
#             if os.path.isfile(ruta_elemento) and elemento.endswith(".exe"):
#                 # Crear un botón para ejecutar el archivo .exe
#                 boton_ejecutar = tk.Button(ventana, text=f"Ejecutar {elemento}", command=lambda exe=ruta_elemento: ejecutar_exe(exe))
#                 boton_ejecutar.pack()

# def ejecutar_exe(ruta_exe):
#     # Ejecutar el archivo .exe
#     print(ruta_exe)
#     os.system(ruta_exe)

# # Crear la ventana principal
# ventana = tk.Tk()
# ventana.title("Listar y Ejecutar Archivos .exe")

# # Botón para seleccionar una carpeta
# boton_seleccionar_carpeta = tk.Button(ventana, text="Seleccionar Carpeta", command=listar_elementos_carpeta)
# boton_seleccionar_carpeta.pack()

# ventana.mainloop()

# --------------------------------------------------------------------------------------------------------------------------------

# import tkinter as tk
# from tkinter import ttk
# from tkinter import messagebox

# # Función para abrir una nueva ventana con un campo de entrada
# def abrir_ventana_input(id):
#     ventana_input = tk.Toplevel(ventana_principal)
#     ventana_input.title(f"Ventana #{id}")
    
#     # Etiqueta e input en la nueva ventana
#     etiqueta = ttk.Label(ventana_input, text="Ingresa algo:")
#     etiqueta.pack(padx=10, pady=5)
    
#     campo_input = ttk.Entry(ventana_input)
#     campo_input.pack(padx=10, pady=5)
    
#     # Función para mostrar el contenido del campo de entrada
#     def mostrar_input():
#         contenido = campo_input.get()
#         messagebox.showinfo("Contenido", f"Input: {contenido} (ID: {id})")
    
#     # Botón para mostrar el contenido del campo de entrada
#     boton_mostrar = ttk.Button(ventana_input, text="Mostrar Input", command=mostrar_input)
#     boton_mostrar.pack(padx=10, pady=10)

# # Crear la ventana principal
# ventana_principal = tk.Tk()
# ventana_principal.title("Tarjetas con Botones y Marcos en Modo Oscuro")

# # Estilo personalizado para los widgets ttk en modo oscuro
# estilo = ttk.Style()
# estilo.configure("TFrame", background="gray10")
# estilo.configure("TLabel", background="gray10", foreground="white")
# estilo.configure("TButton", background="gray20", foreground="white")
# estilo.configure("TEntry", background="gray30", foreground="white")

# # Crear tarjetas con botones y marcos
# for i in range(3):  # Crear 3 tarjetas como ejemplo
#     marco_tarjeta = ttk.Frame(ventana_principal, borderwidth=2, relief="solid")
#     marco_tarjeta.grid(row=i, column=0, padx=10, pady=10, sticky="nsew")  # Hacemos que las tarjetas se expandan
    
#     # Botón para abrir una nueva ventana con input y mostrar el ID
#     id_tarjeta = i + 1  # IDs comenzando desde 1
#     boton_abrir_ventana = ttk.Button(marco_tarjeta, text=f"Abrir Ventana #{id_tarjeta}",command=lambda id=id_tarjeta: abrir_ventana_input(id))
#     boton_abrir_ventana.pack(expand=True, fill="both")
    
#     # Otro botón en la misma tarjeta (puedes personalizarlo según tus necesidades)
#     boton_otro = ttk.Button(marco_tarjeta, text="Otro Botón")
#     boton_otro.pack(expand=True, fill="both")

# # Configurar la expansión de las filas y columnas en la ventana principal
# ventana_principal.grid_rowconfigure(0, weight=1)
# ventana_principal.grid_columnconfigure(0, weight=1)

# ventana_principal.configure(background="gray10")  # Fondo de la ventana principal en modo oscuro

# ventana_principal.mainloop()

# ------------------------------------------------------------------------------------------------------------------------------

# import time
# import threading
# import os

# # Hora definida para la comparación
# hora_definida = "10:35:50"

# def ejecutar_comando():
#     # Obtener la hora actual en formato "HH:MM:SS"
#     hora_actual = time.strftime("%H:%M:%S")
    
#     # Calcular la diferencia en minutos entre la hora definida y la hora actual
#     diferencia_minutos = calcular_diferencia_minutos(hora_definida, hora_actual)
    
#     print(f"Hora definida: {hora_definida}")
#     print(f"Hora actual: {hora_actual}")
#     print(f"Diferencia en minutos: {diferencia_minutos} minutos")

# def calcular_diferencia_minutos(hora_definida, hora_actual):
#     # Parsear las horas en formato "HH:MM:SS" a segundos
#     tiempo_definido = sum(int(x) * 60 ** i for i, x in enumerate(reversed(hora_definida.split(":"))))
#     tiempo_actual = sum(int(x) * 60 ** i for i, x in enumerate(reversed(hora_actual.split(":"))))
    
#     # Calcular la diferencia en segundos y luego convertirla a minutos
#     diferencia_segundos = tiempo_actual - tiempo_definido
#     diferencia_minutos = diferencia_segundos / 60
    
#     return diferencia_minutos

# def verificar_tiempo():
#     while True:
#         tiempo_actual = time.localtime()
#         minutos_actual = tiempo_actual.tm_min
        
#         # Espera hasta que pase un minuto
#         while tiempo_actual.tm_min == minutos_actual:
#             time.sleep(1)
#             tiempo_actual = time.localtime()
        
#         # Ejecuta el comando
#         ejecutar_comando()

# # Iniciar un subproceso para verificar el tiempo
# hilo_tiempo = threading.Thread(target=verificar_tiempo)
# hilo_tiempo.daemon = True
# hilo_tiempo.start()

# # Puedes continuar ejecutando otras tareas en el hilo principal
# # mientras el subproceso verifica el tiempo en segundo plano.

# # Mantén el programa en ejecución
# try:
#     while True:
#         pass
# except KeyboardInterrupt:
#     pass



# ------------------------------------------------------------------------- ULTIMO FUNCIONAL
# import tkinter as tk
# from tkinter import ttk
# from tkinter import messagebox
# from tkinter import filedialog

# # Lista para almacenar las tarjetas creadas
# tarjetas = []

# def seleccionar_archivo(campo_ruta_archivo):
#     archivo_ruta = filedialog.askopenfilename()  # Abre el diálogo de selección de archivo
#     campo_ruta_archivo.delete(0, tk.END)  # Borra el contenido actual del campo de entrada
#     campo_ruta_archivo.insert(0, archivo_ruta)

# def abrir_ventana_input(id):
#     ventana_input = tk.Toplevel(ventana_principal)
#     ventana_input.title(f"Ventana #{id}")
    
#     # Etiqueta e input en la nueva ventana
#     etiqueta = ttk.Label(ventana_input, text="Ingresa algo:")
#     etiqueta.pack(padx=10, pady=5)
    
#     campo_input = ttk.Entry(ventana_input)
#     campo_input.pack(padx=10, pady=5)
    
#     # Función para mostrar el contenido del campo de entrada
#     def mostrar_input():
#         contenido = campo_input.get()
#         messagebox.showinfo("Contenido", f"Input: {contenido} (ID: {id})")
    
#     # Botón para mostrar el contenido del campo de entrada
#     boton_mostrar = ttk.Button(ventana_input, text="Mostrar Input", command=mostrar_input)
#     boton_mostrar.pack(padx=10, pady=10)

# def abrir_tarjeta(id, nombre_tarjeta):
#     def imprimir_datos():
#         intervalo = campo_input.get()
#         dias_seleccionados = [dias_semana[i] for i in lista_dias.curselection()]
#         estado = "Activo" if estado_var.get() else "Inactivo"
#         archivo_ruta = campo_ruta_archivo.get()  # Obtiene la ruta del archivo

#         # Imprimir datos en la consola, incluyendo la ruta del archivo
#         print(f"ID: {id}")
#         print(f"Nombre de la Tarjeta: {nombre_tarjeta}")
#         print(f"Intervalo (Minutos): {intervalo}")
#         print(f"Días seleccionados: {', '.join(dias_seleccionados)}")
#         print(f"Estado: {estado}")
#         print(f"Ruta del Archivo: {archivo_ruta}")

#         # Mostrar ventana emergente de confirmación
#         messagebox.showinfo("Confirmación", "Datos impresos en la consola.\n¡Confirmación exitosa!")

#     #Creacion de la Ventana
#     ventana_tarjeta = tk.Toplevel(ventana_principal)
#     ventana_tarjeta.title(f"Tarjeta #{id} - {nombre_tarjeta}")

#     marco_tarjeta = ttk.Frame(ventana_tarjeta, borderwidth=2, relief="solid")
#     marco_tarjeta.pack(padx=10, pady=10)

#     #Nombre de la tarjeta
#     etiqueta_nombre = ttk.Label(marco_tarjeta, text="Nombre de la Tarjeta:")
#     etiqueta_nombre.grid(row=0, column=0, padx=10, pady=5)

#     campo_nombre = ttk.Entry(marco_tarjeta)
#     campo_nombre.insert(0, nombre_tarjeta)
#     campo_nombre.grid(row=1, column=0, padx=10, pady=5)

#     #Ruta del .exe
#     etiqueta_archivo = ttk.Label(marco_tarjeta, text="Selecciona un archivo:")
#     etiqueta_archivo.grid(row=2, column=0, padx=10, pady=5)

#     campo_ruta_archivo = ttk.Entry(marco_tarjeta)
#     campo_ruta_archivo.grid(row=3, column=0, padx=10, pady=5)

#     boton_seleccionar_archivo = ttk.Button(marco_tarjeta, text="Seleccionar Archivo", command=lambda: seleccionar_archivo(campo_ruta_archivo))
#     boton_seleccionar_archivo.grid(row=4, column=0, padx=10, pady=5)

#     #Input de intervalo de tiempo
#     etiqueta_input = ttk.Label(marco_tarjeta, text="Intervalo (Minutos):")
#     etiqueta_input.grid(row=5, column=0, padx=10, pady=5)

#     campo_input = ttk.Entry(marco_tarjeta)
#     campo_input.grid(row=6, column=0, padx=10, pady=5)

#     #Seleccion de dias de la semana
#     etiqueta_lista = ttk.Label(marco_tarjeta, text="Selecciona uno o más días de la semana:")
#     etiqueta_lista.grid(row=7, column=0, padx=10, pady=5)

#     dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
#     lista_dias = tk.Listbox(marco_tarjeta, selectmode=tk.MULTIPLE)
#     for dia in dias_semana:
#         lista_dias.insert(tk.END, dia)
#     lista_dias.grid(row=8, column=0, padx=10, pady=5)

#     # Seleccion del estado del bot
#     etiqueta_estado = ttk.Label(marco_tarjeta, text="Estado:")
#     etiqueta_estado.grid(row=9, column=0, padx=10, pady=5)

#     estado_var = tk.BooleanVar()
#     estado_var.set(True)  # Inicialmente, el checkbox Activo está marcado como verdadero
#     checkbox_activo = ttk.Checkbutton(marco_tarjeta, text="Activo", variable=estado_var, onvalue=True, offvalue=False)
#     checkbox_activo.grid(row=10, column=0, padx=10, pady=5, sticky="w")

#     checkbox_inactivo = ttk.Checkbutton(marco_tarjeta, text="Inactivo", variable=estado_var, onvalue=False, offvalue=True)
#     checkbox_inactivo.grid(row=11, column=0, padx=10, pady=5, sticky="w")

#     #Boton de recoleccion de datos
#     boton_imprimir = ttk.Button(marco_tarjeta, text="Imprimir Datos y Confirmar", command=imprimir_datos)
#     boton_imprimir.grid(row=12, column=0, padx=10, pady=10)

# def agregar_tarjeta():
#     id_nueva_tarjeta = len(tarjetas) + 1
#     nombre_nueva_tarjeta = f"Tarjeta {id_nueva_tarjeta}"
#     tarjetas.append((id_nueva_tarjeta, nombre_nueva_tarjeta))
    
#     boton_tarjeta = ttk.Button(ventana_principal, text=nombre_nueva_tarjeta, command=lambda id=id_nueva_tarjeta, nombre=nombre_nueva_tarjeta: abrir_tarjeta(id, nombre))
#     boton_tarjeta.pack(expand=True, fill="both")

# # Crear la ventana principal
# ventana_principal = tk.Tk()
# ventana_principal.title("Orquestador")

# # Agregar botón para crear una nueva tarjeta
# boton_nueva_tarjeta = ttk.Button(ventana_principal, text="Crear Nueva Tarjeta", command=agregar_tarjeta)
# boton_nueva_tarjeta.pack(expand=True, fill="both")
# ventana_principal.mainloop()

# -------------------------------------------------------------------------------------------------------------- Ejecucion en cola
