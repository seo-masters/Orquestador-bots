import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import sqlite3
import subprocess
import threading

# Lista para almacenar las tarjetas creadas
tarjetas = []
# lista de procesos en ejecucion
procesos = []
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
        lunes INTEGER NOT NULL,
        martes INTEGER NOT NULL,
        miercoles INTEGER NOT NULL,
        jueves INTEGER NOT NULL,
        viernes INTEGER NOT NULL,
        sabado INTEGER NOT NULL,
        domingo INTEGER NOT NULL,
        last_run TEXT
    );
    ''')

    cursor = conn.cursor()

    return cursor
# creacion de bot base
def nuevo_bot(cursor,container):

    id = len(tarjetas) + 1

    cursor.execute('''
    INSERT INTO bots (name, path, status, interval, lunes, martes, miercoles, jueves, viernes, sabado, domingo, last_run)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (f'Nuevo Bot {id}','c:/','active', 0, 0, 0, 0, 0, 0, 0, 0, "Sin ejecucion"))

    cursor.connection.commit()

    getAll(cursor,container)
# recuperar todo los datos
def getAll(cursor, container):
    global tarjetas
    
    # Borra todos los widgets hijos de la ventana principalk
    for widget in container.winfo_children():
        widget.destroy()

    cursor.execute('SELECT * FROM bots')
    tarjetas = cursor.fetchall()
    
    for bot in tarjetas:

        if bot[3] == 'Activo':
            status = True
        else:
            status = False

        path = bot[2]

        boton_tarjeta = ttk.Button(container, text=bot[1], command=lambda id=bot[0], nombre=bot[1], path=path, param4=bot[4], status=status: abrir_tarjeta(cursor, id, nombre, path, param4, status))
        boton_tarjeta.grid(row=bot[0], column=0, padx=10, pady=5)

        boton_eliminar = ttk.Button(container, text='Eliminar', command=lambda id=bot[0]:eliminar_bot(cursor,id,container) )
        boton_eliminar.grid(row=bot[0], column=1, padx=10, pady=5)
# Verifica que dias estan activos
def verificar_dias(cursor,lista_dias,dias_semana,id):

    cursor.execute('''
            SELECT lunes, martes, miercoles, jueves, viernes, sabado, domingo
            FROM bots
            WHERE id = ?
        ''', (id,)) 
    
    valores = cursor.fetchall()

    actualizar_seleccion(lista_dias,dias_semana,valores[0])
#Limpia la seleccion de dias activos
def reset_dias(cursor,lista_dias,dias_semana,id):
    for dia in dias_semana:
        diaUpdate = dia.lower()

        cursor.execute(f'''
        UPDATE bots
        SET {diaUpdate} = ?
        WHERE id= ?
        ''', (0,id))

        cursor.connection.commit()
    
    verificar_dias(cursor,lista_dias,dias_semana,id)
# Recibe todos los datos que se hayan hecho y los sube a la base de datos
def actualizar_datos(cursor,id,campo_nombre,campo_input,dias_semana,lista_dias,estado_var,campo_ruta_archivo,ventana_principal):
    new_name = campo_nombre.get()
    new_interval = campo_input.get()
    dias_seleccionados = [dias_semana[i] for i in lista_dias.curselection()]
    new_status = "Activo" if estado_var.get() else "Inactivo"
    new_path = campo_ruta_archivo.get()  # Obtiene la ruta del archivo

    try:

        for dia in dias_seleccionados:
            diaUpdate = dia.lower()

            cursor.execute(f'''
            UPDATE bots
            SET {diaUpdate} = ?
            WHERE id= ?
            ''', (1,id))
        
        cursor.execute('''
        UPDATE bots
        SET name=?, path=?, status=?, interval=?
        WHERE id=?
        ''', (new_name, new_path, new_status, new_interval, id))

        cursor.connection.commit()

        verificar_dias(cursor,lista_dias,dias_semana,id)

        getAll(cursor, ventana_principal)

        messagebox.showinfo("Confirmación", "Datos actualizados\n¡Configuracion exitosa!")

    except Exception as e:
        print(e)
        messagebox.showinfo("Error", "No se pudieron actulizar los datos.\nActualizacion fallida")
#Eliminar Bot
def eliminar_bot(cursor,id,contenedor_botones):
    try:
        cursor.execute('DELETE FROM bots WHERE id = ?', (id,))
        cursor.connection.commit() 
        getAll(cursor,contenedor_botones)
        messagebox.showinfo("Confirmación", "Bot Borrado\n¡Eliminacion exitosa!")
    except:
        messagebox.showinfo("Error", "No se pudo borrar el dato.\Eliminacion fallida")

## Frontend
# Permite la seleccion de la ruta
def seleccionar_archivo(campo_ruta_archivo):
    archivo_ruta = filedialog.askopenfilename()  # Abre el diálogo de selección de archivo
    campo_ruta_archivo.delete(0, tk.END)  # Borra el contenido actual del campo de entrada
    campo_ruta_archivo.insert(0, archivo_ruta)
# Abre la tarjeta de configuracion del bot
def abrir_tarjeta(cursor, id, nombre_tarjeta, path_pred, intervalo_pred, status): 
    #Creacion de la Ventana
    ventana_tarjeta = tk.Toplevel(contenedor_botones)
    ventana_tarjeta.title(f"Bot #{id} - {nombre_tarjeta}")

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
    campo_ruta_archivo.insert(0, path_pred) 
    campo_ruta_archivo.grid(row=3, column=0, padx=10, pady=5)

    boton_seleccionar_archivo = ttk.Button(marco_tarjeta, text="Seleccionar Archivo", command=lambda: seleccionar_archivo(campo_ruta_archivo))
    boton_seleccionar_archivo.grid(row=4, column=0, padx=10, pady=5)

    #Input de intervalo de tiempo
    etiqueta_input = ttk.Label(marco_tarjeta, text="Intervalo (Minutos):")
    etiqueta_input.grid(row=5, column=0, padx=10, pady=5)

    campo_input = ttk.Entry(marco_tarjeta)
    campo_input.insert(0, intervalo_pred) 
    campo_input.grid(row=6, column=0, padx=10, pady=5)

    #Seleccion de dias de la semana
    dias_semana = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
    etiqueta_lista = ttk.Label(marco_tarjeta, text="Selecciona uno o más días de la semana:")
    etiqueta_lista.grid(row=7, column=0, padx=10, pady=5)

    lista_dias = tk.Listbox(marco_tarjeta, selectmode=tk.MULTIPLE)
    for dia in dias_semana:
        lista_dias.insert(tk.END, dia)
    lista_dias.grid(row=8, column=0, padx=10, pady=5)
    
    verificar_dias(cursor,lista_dias,dias_semana,id)

    boton_reset_dias = ttk.Button(marco_tarjeta, text="Reset dias", command=lambda: reset_dias(cursor,lista_dias,dias_semana,id))
    boton_reset_dias.grid(row=9, column=0, padx=10, pady=5)

    # Seleccion del estado del bot
    etiqueta_estado = ttk.Label(marco_tarjeta, text="Estado:")
    etiqueta_estado.grid(row=10, column=0, padx=10, pady=5)

    estado_var = tk.BooleanVar()
    estado_var.set(status)  # Inicialmente, el checkbox Activo está marcado como verdadero
    checkbox_activo = ttk.Checkbutton(marco_tarjeta, text="Activo", variable=estado_var, onvalue=True, offvalue=False)
    checkbox_activo.grid(row=11, column=0, padx=10, pady=5, sticky="w")

    checkbox_inactivo = ttk.Checkbutton(marco_tarjeta, text="Inactivo", variable=estado_var, onvalue=False, offvalue=True)
    checkbox_inactivo.grid(row=12, column=0, padx=10, pady=5, sticky="w")

    boton_ejecutar = ttk.Button(marco_tarjeta, text="Correr", command=lambda: boton_correr(campo_ruta_archivo))
    boton_ejecutar.grid(row=13, column=0, padx=10, pady=10)

    #Boton de recoleccion de datos
    boton_imprimir = ttk.Button(marco_tarjeta, text="Actualizar", command=lambda: actualizar_datos(cursor,id ,campo_nombre, campo_input,dias_semana,lista_dias,estado_var,campo_ruta_archivo,contenedor_botones))
    boton_imprimir.grid(row=14, column=0, padx=10, pady=10)
# Seleccion de creacion 
def actualizar_seleccion(lista_dias, dias_semana, valores):
    for i in range(len(dias_semana)):
        valor = valores[i]
        color_fondo = 'lightblue' if valor == 1 else 'white'
        lista_dias.itemconfig(i, {'bg': color_fondo})

# Ejecuta el bot.exe
def correr_bot(path):
    try:
        subprocess.Popen(path, shell=True)
        print("El archivo .exe se ha ejecutado en segundo plano.")
    except Exception as e:
        print(f"Error al ejecutar el archivo .exe: {str(e)}")

#Ejecuta el bot en un hilo 
def ejecutar_bot_en_hilo(path):
    hilo = threading.Thread(target=correr_bot, args=(path,))
    hilo.start()

#Disparador que recibe la ruta y ejeuta el bot
def boton_correr(campo_ruta_archivo):
    ruta_al_exe = campo_ruta_archivo.get()
    ejecutar_bot_en_hilo(ruta_al_exe)

try:

    if __name__ == "__main__":
        #Inicilizo la base de datos
        cursor = init_db()

        ventana_principal = tk.Tk()
        ventana_principal.title("Orquestador")

        # Creación de botón para crear un nuevo bot
        boton_nueva_tarjeta = ttk.Button(ventana_principal, text="Crear Nuevo Bot", command=lambda: nuevo_bot(cursor, contenedor_botones))
        boton_nueva_tarjeta.pack(expand=True, fill="both")

        # Contenedor para los botones de los bots
        contenedor_botones = ttk.Frame(ventana_principal)
        contenedor_botones.pack()

        # Creación de botón para actualizar la vista
        boton_actualizar_vista = ttk.Button(ventana_principal, text="Actulizar", command=lambda: getAll(cursor, contenedor_botones))
        boton_actualizar_vista.pack(expand=True, fill="both")


        # Llamar a la función getAll una vez para inicializar la lista de botones
        getAll(cursor, contenedor_botones)

        # Mantener la ventana principal abierta
        ventana_principal.mainloop()

except Exception as e:
    print(e)