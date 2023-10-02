import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import sqlite3

# Lista para almacenar las tarjetas creadas
tarjetas = []

## Base de datos
def init_db():
    conn = sqlite3.connect('Orquestador.db')

    # Creación de la tabla "bots"
    conn.execute('''
    CREATE TABLE IF NOT EXISTS bots (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        path TEXT NOT NULL,
        status TEXT NOT NULL,
        interval INTEGER NOT NULL,
        l INTEGER NOT NULL,
        m INTEGER NOT NULL,
        x INTEGER NOT NULL,
        j INTEGER NOT NULL,
        v INTEGER NOT NULL,
        last_run TEXT
    );
    ''')

    cursor = conn.cursor()

    return cursor
# creacion de bot base
def nuevo_bot(cursor,ventana_principal):

    id = len(tarjetas) + 1

    cursor.execute('''
    INSERT INTO bots (name, path, status, interval, l, m, x, j, v, last_run)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (f'Nuevo Bot {id}','c:/','active', 0, 0, 0, 0, 0, 0, "Sin ejecucion"))

    cursor.connection.commit()

    getAll(cursor,ventana_principal)
# recuperar todo los datos
def getAll(cursor, ventana_principal):
    global tarjetas
    cursor.execute('SELECT * FROM bots')
    tarjetas = cursor.fetchall()

    for bot in tarjetas:
        boton_tarjeta = ttk.Button(ventana_principal, text=bot[1], command=lambda id=bot[0], nombre=bot[1]: abrir_tarjeta(cursor, id, nombre))
        boton_tarjeta.pack(expand=True, fill="both")

def actualizar_datos(cursor,id,nombre_tarjeta,campo_input,dias_semana,lista_dias,estado_var,campo_ruta_archivo):
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


## Frontend
def seleccionar_archivo(campo_ruta_archivo):
    archivo_ruta = filedialog.askopenfilename()  # Abre el diálogo de selección de archivo
    campo_ruta_archivo.delete(0, tk.END)  # Borra el contenido actual del campo de entrada
    campo_ruta_archivo.insert(0, archivo_ruta)

def abrir_tarjeta(cursor, id, nombre_tarjeta):

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
    etiqueta_archivo = ttk.Label(marco_tarjeta, text="Selecciona path archivo:")
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
    boton_imprimir = ttk.Button(marco_tarjeta, text="Imprimir Datos y Confirmar", command=lambda: actualizar_datos(cursor,id ,nombre_tarjeta, campo_input,dias_semana,lista_dias,estado_var,campo_ruta_archivo))
    boton_imprimir.grid(row=12, column=0, padx=10, pady=10)


try:
    #Inicilizo la base de datos
    cursor = init_db()

    # Creacion de la ventana principal
    ventana_principal = tk.Tk()
    ventana_principal.title("Orquestador")

    #Creacion boton de agregar bot
    boton_nueva_tarjeta = ttk.Button(ventana_principal, text="Crear Nuevo Bot",  command=lambda: nuevo_bot(cursor, ventana_principal))
    boton_nueva_tarjeta.pack(expand=True, fill="both")

    #REcupera todos los datos de la base de datos
    getAll(cursor,ventana_principal)

    # Agregar botón para crear una nueva tarjeta

    ventana_principal.mainloop()

except Exception as e:
    print(e)
# Crear la ventana principal
