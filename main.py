from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from skpy import Skype
import tkinter as tk
import sqlite3
import subprocess
import threading
import time
import datetime

# Lista para almacenar las tarjetas creadas
tarjetas = []
# lista de procesos en ejecucion
procesos = []
# Variable global para almacenar la hora de finalización
hora_finalizacion = None

while True:

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
        # Creación de la tabla "logs"
        conn.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY,
                name_bot TEXT NOT NULL,
                date TEXT NOT NULL,
                mensaje TEXT NOT NULL,
                type TEXT NOT NULL
            );
            ''')
        
        cursor = conn.cursor()

        return cursor

    #Registro de log
    def log(name, mensaje, type):

        conexion = sqlite3.connect("Orquestador.db")
        cursor = conexion.cursor()
        
        # Obtener la fecha y hora actual
        fecha_hora_actual = datetime.datetime.now()

        # Formatear la fecha y hora en el formato deseado
        fecha_hora_formateada = fecha_hora_actual.strftime("%d/%m/%y %H:%M:%S")

            
        cursor.execute('INSERT INTO logs (name_bot, date, mensaje, type) VALUES (?, ?, ?, ?)', (name, fecha_hora_formateada, mensaje, type))

        cursor.connection.commit()

        conexion.close()

    # recuperar todo los datos
    def getAll(cursor, container):
        try:

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

                log('getAll', 'Se obtuviero todo los bots registrados', 'CONFIG')
        except Exception as e:
            log('getAll', str(e), 'ERROR')

    # creacion de bot base
    def nuevo_bot(cursor,container):
        try:
            id = len(tarjetas) + 1

            cursor.execute('''
            INSERT INTO bots (name, path, status, interval, lunes, martes, miercoles, jueves, viernes, sabado, domingo, last_run)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (f'Nuevo Bot {id}','c:/','Inactivo', 0, 0, 0, 0, 0, 0, 0, 0, "Sin ejecucion"))


            cursor.connection.commit()

            log('nuevo_bot', 'Crecion exitosa de nuevo bot', 'CONFIG')

            getAll(cursor,container)
        except Exception as e:
            log('nuevo_bot', str(e), 'ERROR')

    # Verifica que dias estan activos
    def verificar_dias(cursor,lista_dias,dias_semana,id):
        try:
            cursor.execute('''
                    SELECT lunes, martes, miercoles, jueves, viernes, sabado, domingo
                    FROM bots
                    WHERE id = ?
                ''', (id,)) 
            
            valores = cursor.fetchall()

            actualizar_seleccion(lista_dias,dias_semana,valores[0])

            log('verificar_dias', 'Verificacion de dias activos', 'CONFIG')

        except Exception as e:
            log('verificar_dias', str(e), 'ERROR')
    
    #Limpia la seleccion de dias activos
    def reset_dias(cursor,lista_dias,dias_semana,id):
        try:
            for dia in dias_semana:
                diaUpdate = dia.lower()

                cursor.execute(f'''
                UPDATE bots
                SET {diaUpdate} = ?
                WHERE id= ?
                ''', (0,id))

                cursor.connection.commit()
            
            verificar_dias(cursor,lista_dias,dias_semana,id)

            log('reset_dias', f'Limpia la seleccion de dias activos en bot: {id}', 'CONFIG')
        except Exception as e:
            log('reset_dias', str(e), 'ERROR')

    # Recibe todos los datos que se hayan hecho y los sube a la base de datos
    def actualizar_datos(cursor,id,campo_nombre,campo_input,dias_semana,lista_dias,estado_var,campo_ruta_archivo,ventana_principal):
        try:
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

                log('actualizar_datos', f'Configuracion actualizada de bot {id}', 'CONFIG')

                messagebox.showinfo("Confirmación", "Datos actualizados\n¡Configuracion exitosa!")

            except Exception as e:
                log('actualizar_datos', str(e), 'ERROR')
                messagebox.showinfo("Error", "No se pudieron actulizar los datos.\nActualizacion fallida")

        except Exception as e:
            log('actualizar_datos', str(e), 'ERROR')
    
    # Eliminar Bot
    def eliminar_bot(cursor,id,contenedor_botones):
        try:
            cursor.execute('DELETE FROM bots WHERE id = ?', (id,))
            cursor.connection.commit() 
            getAll(cursor,contenedor_botones)
            log('eliminar_bot', f'Bot {id} borrado', 'CONFIG')
            messagebox.showinfo("Confirmación", "Bot Borrado\n¡Eliminacion exitosa!")
        except:
            log('eliminar_bot', str(e), 'ERROR')
            messagebox.showinfo("Error", "No se pudo borrar el dato.\Eliminacion fallida")
    
    # Actualiza el campo de last_run de cada bot
    def actualizar_last_run(bot_id, last_run_value):
        try:
            # Crear y abrir la conexión a la base de datos en este hilo
            conexion = sqlite3.connect("Orquestador.db")
            cursor = conexion.cursor()

            cursor.execute('UPDATE bots SET last_run = ? WHERE id = ?', (last_run_value, bot_id))
            conexion.commit()

            # Cerrar la conexión después de usarla
            conexion.close()
        except Exception as e:
            print(f"Error al ejecutar la actualización en la base de datos: {str(e)}")

    # Obtienen los intervalos y el last_run
    def get_intervalo_last_run():
        try:
            conexion = sqlite3.connect("Orquestador.db")
            cursor = conexion.cursor()
        
            cursor.execute('SELECT name, interval, last_run, status, path, id FROM bots')
            result = cursor.fetchall()  # Recuperar la primera fila como una tupla

            cursor.execute('''
                    SELECT lunes, martes, miercoles, jueves, viernes, sabado, domingo
                    FROM bots
                    WHERE id = ?
                ''', (result[0][5],))   
            valores = cursor.fetchall()

            if result:
                return result, valores[0]
            else:
                return None  # El bot con el ID proporcionado no se encontró en la base de datos
        except Exception as e:
            print(f"Error al ejecutar la consulta en la base de datos: {str(e)}")

    ## Frontend

    # Permite la seleccion de la ruta
    def seleccionar_archivo(campo_ruta_archivo):
        try:
            archivo_ruta = filedialog.askopenfilename()  # Abre el diálogo de selección de archivo
            campo_ruta_archivo.delete(0, tk.END)  # Borra el contenido actual del campo de entrada
            campo_ruta_archivo.insert(0, archivo_ruta)
            log('seleccionar_archivo', 'Seleccion de ruta', 'CONFIG')
        except Exception as e:
            log('seleccionar_archivo', str(e), 'ERROR')
    
    # Abre la tarjeta de configuracion del bot
    def abrir_tarjeta(cursor, id, nombre_tarjeta, path_pred, intervalo_pred, status): 

        try:
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

            boton_ejecutar = ttk.Button(marco_tarjeta, text="Correr", command=lambda: boton_correr(id,campo_ruta_archivo))
            boton_ejecutar.grid(row=13, column=0, padx=10, pady=10)

            #Boton de recoleccion de datos
            boton_imprimir = ttk.Button(marco_tarjeta, text="Actualizar", command=lambda: actualizar_datos(cursor,id ,campo_nombre, campo_input,dias_semana,lista_dias,estado_var,campo_ruta_archivo,contenedor_botones))
            boton_imprimir.grid(row=14, column=0, padx=10, pady=10)

            log('nuevo_bot', f'Configuracion abierta de Bot: {id}', 'CONFIG')

        except Exception as e:

            log('abrir_tarjeta', str(e), 'ERROR')
    
    # Seleccion de creacion 
    def actualizar_seleccion(lista_dias, dias_semana, valores):
        try:
            for i in range(len(dias_semana)):
                valor = valores[i]
                color_fondo = 'lightblue' if valor == 1 else 'white'
                lista_dias.itemconfig(i, {'bg': color_fondo})
        except Exception as e:
            log('actualizar_seleccion', str(e), 'ERROR')

    ## Ejecucion de bots

    # Disparador que recibe la ruta y ejeuta el bot
    def boton_correr(id,campo_ruta_archivo):
        try: 
            ruta_al_exe = campo_ruta_archivo.get()
            ejecutar_bot_en_hilo(id,ruta_al_exe)
        except Exception as e:
            log('boton_correr', str(e), 'ERROR')
    
    #Ejecuta el bot en un hilo 
    def ejecutar_bot_en_hilo(id,path):
        try:
            hilo = threading.Thread(target=correr_bot, args=(id,path))
            hilo.start()
            
            log('ejecutar_bot_en_hilo', f'Ejecucion de Bot: {id} en Hilo: {hilo.ident}', 'CONFIG')
        except Exception as e:
            log('ejecutar_bot_en_hilo', str(e), 'ERROR')

    # Ejecuta el bot.exe
    def correr_bot(id,path):
        try:
            hora_actual = time.strftime("%H:%M:%S")
            reporte_skype(id, f'Bot Ejecutado: {hora_actual}')
            proceso = subprocess.Popen(path, shell=True)
            proceso.wait()  # Esperar a que el proceso termine
            log('correr_bot', f'Ejecucion de Bot: {id}', 'EJECUCION')  

            global hora_finalizacion

            hora_actual = time.strftime("%H:%M:%S")
            hora_finalizacion = hora_actual

            actualizar_last_run(id, hora_actual)

            log('correr_bot', f'Bot finalizado: {hora_actual} Bot {id}', 'FINALIZACION')
            reporte_skype(id, f'Bot finalizado: {hora_actual}')

        except Exception as e:
            log('correr_bot', str(e), 'ERROR')

    ###Comparacion de bots en segundo plano

    def dia_semana_hoy():
        # Diccionario para traducir los nombres de los días al español
        days_es = {
            "Monday": "Lunes",
            "Tuesday": "Martes",
            "Wednesday": "Miércoles",
            "Thursday": "Jueves",
            "Friday": "Viernes",
            "Saturday": "Sábado",
            "Sunday": "Domingo",
        }

        # Obtener el día actual
        today = datetime.datetime.today().strftime('%A')
        today_es = days_es[today]

        return today_es

    def calcular_diferencia_minutos(hora_definida, hora_actual):

        try:
            # Parsear las horas en formato "HH:MM:SS" a segundos
            tiempo_definido = sum(int(x) * 60 ** i for i, x in enumerate(reversed(hora_definida.split(":"))))
            tiempo_actual = sum(int(x) * 60 ** i for i, x in enumerate(reversed(hora_actual.split(":"))))
            
            # Calcular la diferencia en segundos y luego convertirla a minutos
            diferencia_segundos = tiempo_actual - tiempo_definido
            diferencia_minutos = diferencia_segundos / 60
        
            return diferencia_minutos
        except Exception as e:
            log('calcular_diferencia_minutos', str(e), 'ERROR')
    
    def ejecutar_bot_programado():
        try:
            hora_actual = time.strftime("%H:%M:%S")

            bots,valores_dias  = get_intervalo_last_run()

            for bot in bots:

                dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

                # Convertir valores binarios a nombres de días de la semana
                dias_seleccionados = [dias_semana[i] for i, valor in enumerate(valores_dias) if valor == 1]

                today = dia_semana_hoy()
                
                program_day = today in dias_seleccionados

                if program_day:

                    try: 

                        nombre_bot = bot[0]
                        interval = bot[1]
                        hora_definida = bot[2]
                        status = bot[3]
                        path = bot[4]
                        id = bot[5]


                        def calculo_Ejecucion():

                            diferencia_minutos = calcular_diferencia_minutos(hora_definida, hora_actual)

                            if diferencia_minutos >= interval:

                                ejecutar_bot_en_hilo(id,path)

                        if hora_definida == 'Sin ejecucion':
                            if status == 'Activo':
                                print(f'Primera ejecucion bot: {nombre_bot}')
                                ejecutar_bot_en_hilo(id,path)
                            else:
                                pass
                        else:
                            if status == 'Activo':
                                calculo_Ejecucion()
                            else:
                                pass
                    
                    except Exception as e:
                        print(f'ejecutar_bot_programado - Error al ejecutar bot {bot[5]} :  {str(e)}')
            
        except Exception as e:  
            log('ejecutar_bot_programado',f'ejecutar_bot_programado {str(e)}' ,'ERROR')

    def auto_ejecucion():
        try:
            while True:
                tiempo_actual = time.localtime()
                minutos_actual = tiempo_actual.tm_min
                
                # Espera hasta que pase un minuto
                while tiempo_actual.tm_min == minutos_actual:
                    time.sleep(1)
                    tiempo_actual = time.localtime()
                
                # Ejecuta el comando
                ejecutar_bot_programado()
        except Exception as e:
            print(f'auto_ejecucion {str(e)}  ERROR')

    def init_programacion_bots():
        try:
            hilo_tiempo = threading.Thread(target=auto_ejecucion)
            hilo_tiempo.daemon = True
            hilo_tiempo.start()
        except Exception as e:
            log('init_programacion_bots', str(e), 'ERROR')

    ###Skype

    def reporte_skype(id,msg):

        slogin = Skype("cs009@skycellular.net","aztecaintvalentina2019")
        contact = slogin.chats['19:15ded9b221e745c4831b6b1441cfb8bf@thread.skype']
        contact.sendMsg(f'{msg} - Bot: {id}')

    try:

        if __name__ == "__main__":
            #Inicilizo la base de datos
            cursor = init_db()

            init_programacion_bots()

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
        log('Main', str(e), 'ERROR')