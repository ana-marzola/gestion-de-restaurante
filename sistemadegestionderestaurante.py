import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# Conexión a la base de datos
def conectar_db():
    try:
        conexion = mysql.connector.connect(
            host="localhost",  # Cambia por tu host si es necesario
            user="root",       # Cambia por tu usuario de MySQL
            password="",       # Cambia por tu contraseña
            database="restaurante_db"
        )
        return conexion
    except mysql.connector.Error as err:
        messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos: {err}")
        return None

# Función para cargar mesas disponibles
def cargar_mesas():
    conexion = conectar_db()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT mesa_id, numero_mesa FROM mesas WHERE estado = 'Disponible'")
        mesas = cursor.fetchall()
        conexion.close()
        return mesas
    return []

# Función para registrar una nueva mesa
def registrar_mesa():
    numero_mesa = entry_numero_mesa.get()
    ubicacion = entry_ubicacion.get()

    if not (numero_mesa and ubicacion):
        messagebox.showwarning("Campos vacíos", "Por favor completa todos los campos.")
        return

    conexion = conectar_db()
    if conexion:
        try:
            cursor = conexion.cursor()
            
            # Validar si el número de mesa ya existe
            cursor.execute("SELECT COUNT(*) FROM mesas WHERE numero_mesa = %s", (numero_mesa,))
            existe_mesa = cursor.fetchone()[0]
            
            if existe_mesa > 0:
                messagebox.showerror("Número de mesa duplicado", "El número de mesa ya existe. Ingresa otro número.")
                conexion.close()
                return

            # Insertar la nueva mesa
            cursor.execute(
                "INSERT INTO mesas (numero_mesa, ubicacion) VALUES (%s, %s)",
                (numero_mesa, ubicacion)
            )
            conexion.commit()
            messagebox.showinfo("Éxito", "Mesa registrada exitosamente.")
            conexion.close()
            cargar_mesas_en_combo()  # Refrescar el combo de mesas disponibles
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo registrar la mesa: {err}")
            conexion.rollback()
            conexion.close()

# Función para registrar una reservación
def registrar_reservacion():
    nombre_cliente = entry_nombre.get()
    fecha = entry_fecha.get()
    hora = entry_hora.get()
    numero_mesa = combo_mesas.get()

    if not (nombre_cliente and fecha and hora and numero_mesa):
        messagebox.showwarning("Campos vacíos", "Por favor completa todos los campos.")
        return

    conexion = conectar_db()
    if conexion:
        try:
            cursor = conexion.cursor()

            # Obtener mesa_id usando el número de mesa
            cursor.execute("SELECT mesa_id, estado FROM mesas WHERE numero_mesa = %s", (numero_mesa,))
            mesa = cursor.fetchone()

            if not mesa:
                messagebox.showerror("Mesa no encontrada", "La mesa seleccionada no existe.")
                conexion.close()
                return

            mesa_id, estado_mesa = mesa
            if estado_mesa != 'Disponible':
                messagebox.showerror("Mesa no disponible", "La mesa seleccionada ya está reservada. Elige otra mesa.")
                conexion.close()
                return

            # Insertar la reservación
            cursor.execute(
                "INSERT INTO reservaciones (nombre_cliente, fecha_reserva, hora_reserva, mesa_id) VALUES (%s, %s, %s, %s)",
                (nombre_cliente, fecha, hora, mesa_id)
            )
            # Actualizar el estado de la mesa
            cursor.execute(
                "UPDATE mesas SET estado = 'Reservada' WHERE mesa_id = %s",
                (mesa_id,)
            )
            conexion.commit()
            messagebox.showinfo("Éxito", "Reservación registrada exitosamente.")
            conexion.close()
            cargar_mesas_en_combo()  # Refrescar el combo de mesas disponibles
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo registrar la reservación: {err}")
            conexion.rollback()
            conexion.close()

# Función para cargar mesas en el combobox
def cargar_mesas_en_combo():
    mesas = cargar_mesas()
    combo_mesas["values"] = [mesa[1] for mesa in mesas]  # Listar solo los números de mesa

# Crear la interfaz gráfica
app = tk.Tk()
app.title("Gestión de Reservaciones y Mesas")
app.geometry("500x400")

# Sección de reservaciones
tk.Label(app, text="Gestión de Reservaciones", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

tk.Label(app, text="Nombre del Cliente:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
entry_nombre = tk.Entry(app)
entry_nombre.grid(row=1, column=1, padx=10, pady=5)

tk.Label(app, text="Fecha (YYYY-MM-DD):").grid(row=2, column=0, padx=10, pady=5, sticky="w")
entry_fecha = tk.Entry(app)
entry_fecha.grid(row=2, column=1, padx=10, pady=5)

tk.Label(app, text="Hora (HH:MM):").grid(row=3, column=0, padx=10, pady=5, sticky="w")
entry_hora = tk.Entry(app)
entry_hora.grid(row=3, column=1, padx=10, pady=5)

tk.Label(app, text="Mesa Disponible:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
combo_mesas = ttk.Combobox(app, state="readonly")
combo_mesas.grid(row=4, column=1, padx=10, pady=5)

btn_reservar = tk.Button(app, text="Reservar", command=registrar_reservacion)
btn_reservar.grid(row=5, column=0, columnspan=2, pady=10)

# Sección de mesas
tk.Label(app, text="Gestión de Mesas", font=("Arial", 14, "bold")).grid(row=6, column=0, columnspan=2, pady=10)

tk.Label(app, text="Número de Mesa:").grid(row=7, column=0, padx=10, pady=5, sticky="w")
entry_numero_mesa = tk.Entry(app)
entry_numero_mesa.grid(row=7, column=1, padx=10, pady=5)

tk.Label(app, text="Ubicación:").grid(row=8, column=0, padx=10, pady=5, sticky="w")
entry_ubicacion = tk.Entry(app)
entry_ubicacion.grid(row=8, column=1, padx=10, pady=5)

btn_agregar_mesa = tk.Button(app, text="Agregar Mesa", command=registrar_mesa)
btn_agregar_mesa.grid(row=9, column=0, columnspan=2, pady=10)

# Cargar mesas al iniciar la aplicación
cargar_mesas_en_combo()

app.mainloop()