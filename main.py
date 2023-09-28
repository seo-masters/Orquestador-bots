import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

# Lista para almacenar las tarjetas creadas
tarjetas = []

def seleccionar_archivo(campo_ruta_archivo):
    archivo_ruta = filedialog.askopenfilename()  # Abre el diálogo de selección de archivo
    campo_ruta_archivo.delete(0, tk.END)  # Borra el contenido actual del campo de entrada
    campo_ruta_archivo.insert(0, archivo_ruta)

def abrir_ventana_input(id):
    ventana_input = tk.Toplevel(ventana_principal)
    ventana_input.title(f"Ventana #{id}")
    
    # Etiqueta e input en la nueva ventana
    etiqueta = ttk.Label(ventana_input, text="Ingresa algo:")
    etiqueta.pack(padx=10, pady=5)
    
    campo_input = ttk.Entry(ventana_input)
    campo_input.pack(padx=10, pady=5)
    
    # Función para mostrar el contenido del campo de entrada
    def mostrar_input():
        contenido = campo_input.get()
        messagebox.showinfo("Contenido", f"Input: {contenido} (ID: {id})")
    
    # Botón para mostrar el contenido del campo de entrada
    boton_mostrar = ttk.Button(ventana_input, text="Mostrar Input", command=mostrar_input)
    boton_mostrar.pack(padx=10, pady=10)

def abrir_tarjeta(id, nombre_tarjeta):
    def imprimir_datos():
        intervalo = campo_input.get()
        dias_seleccionados = [dias_semana[i] for i in lista_dias.curselection()]
        estado = "Activo" if estado_var.get() else "Inactivo"
        archivo_ruta = campo_ruta_archivo.get()  # Obtiene la ruta del archivo

        # Imprimir datos en la consola, incluyendo la ruta del archivo
        print(f"ID: {id}")
        print(f"Nombre de la Tarjeta: {nombre_tarjeta}")
        print(f"Intervalo (Minutos): {intervalo}")
        print(f"Días seleccionados: {', '.join(dias_seleccionados)}")
        print(f"Estado: {estado}")
        print(f"Ruta del Archivo: {archivo_ruta}")

        # Mostrar ventana emergente de confirmación
        messagebox.showinfo("Confirmación", "Datos impresos en la consola.\n¡Confirmación exitosa!")

    #Creacion de la Ventana
    ventana_tarjeta = tk.Toplevel(ventana_principal)
    ventana_tarjeta.title(f"Tarjeta #{id} - {nombre_tarjeta}")

    marco_tarjeta = ttk.Frame(ventana_tarjeta, borderwidth=2, relief="solid")
    marco_tarjeta.pack(padx=10, pady=10)

    #Nombre de la tarjeta
    etiqueta_nombre = ttk.Label(marco_tarjeta, text="Nombre de la Tarjeta:")
    etiqueta_nombre.grid(row=0, column=0, padx=10, pady=5)

    campo_nombre = ttk.Entry(marco_tarjeta)
    campo_nombre.insert(0, nombre_tarjeta)
    campo_nombre.grid(row=1, column=0, padx=10, pady=5)

    #Ruta del .exe
    etiqueta_archivo = ttk.Label(marco_tarjeta, text="Selecciona un archivo:")
    etiqueta_archivo.grid(row=2, column=0, padx=10, pady=5)

    campo_ruta_archivo = ttk.Entry(marco_tarjeta)
    campo_ruta_archivo.grid(row=3, column=0, padx=10, pady=5)

    boton_seleccionar_archivo = ttk.Button(marco_tarjeta, text="Seleccionar Archivo", command=lambda: seleccionar_archivo(campo_ruta_archivo))
    boton_seleccionar_archivo.grid(row=4, column=0, padx=10, pady=5)

    #Input de intervalo de tiempo
    etiqueta_input = ttk.Label(marco_tarjeta, text="Intervalo (Minutos):")
    etiqueta_input.grid(row=5, column=0, padx=10, pady=5)

    campo_input = ttk.Entry(marco_tarjeta)
    campo_input.grid(row=6, column=0, padx=10, pady=5)

    #Seleccion de dias de la semana
    etiqueta_lista = ttk.Label(marco_tarjeta, text="Selecciona uno o más días de la semana:")
    etiqueta_lista.grid(row=7, column=0, padx=10, pady=5)

    dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    lista_dias = tk.Listbox(marco_tarjeta, selectmode=tk.MULTIPLE)
    for dia in dias_semana:
        lista_dias.insert(tk.END, dia)
    lista_dias.grid(row=8, column=0, padx=10, pady=5)

    # Seleccion del estado del bot
    etiqueta_estado = ttk.Label(marco_tarjeta, text="Estado:")
    etiqueta_estado.grid(row=9, column=0, padx=10, pady=5)

    estado_var = tk.BooleanVar()
    estado_var.set(True)  # Inicialmente, el checkbox Activo está marcado como verdadero
    checkbox_activo = ttk.Checkbutton(marco_tarjeta, text="Activo", variable=estado_var, onvalue=True, offvalue=False)
    checkbox_activo.grid(row=10, column=0, padx=10, pady=5, sticky="w")

    checkbox_inactivo = ttk.Checkbutton(marco_tarjeta, text="Inactivo", variable=estado_var, onvalue=False, offvalue=True)
    checkbox_inactivo.grid(row=11, column=0, padx=10, pady=5, sticky="w")

    #Boton de recoleccion de datos
    boton_imprimir = ttk.Button(marco_tarjeta, text="Imprimir Datos y Confirmar", command=imprimir_datos)
    boton_imprimir.grid(row=12, column=0, padx=10, pady=10)

def agregar_tarjeta():
    id_nueva_tarjeta = len(tarjetas) + 1
    nombre_nueva_tarjeta = f"Tarjeta {id_nueva_tarjeta}"
    tarjetas.append((id_nueva_tarjeta, nombre_nueva_tarjeta))
    
    boton_tarjeta = ttk.Button(ventana_principal, text=nombre_nueva_tarjeta, command=lambda id=id_nueva_tarjeta, nombre=nombre_nueva_tarjeta: abrir_tarjeta(id, nombre))
    boton_tarjeta.pack(expand=True, fill="both")

# Crear la ventana principal
ventana_principal = tk.Tk()
ventana_principal.title("Orquestador")

# Agregar botón para crear una nueva tarjeta
boton_nueva_tarjeta = ttk.Button(ventana_principal, text="Crear Nueva Tarjeta", command=agregar_tarjeta)
boton_nueva_tarjeta.pack(expand=True, fill="both")
ventana_principal.mainloop()
