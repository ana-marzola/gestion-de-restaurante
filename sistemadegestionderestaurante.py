# app_restaurante.py

import mysql.connector
import time
from datetime import datetime


def conectar_bd():
    """
    Función para establecer la conexión con la base de datos.
    Retorna el objeto 'connection' y 'cursor' para interactuar con la DB.
    """
    try:
        # Establecer la conexión con la base de datos
        conexion = mysql.connector.connect(
            host="localhost",  # Cambiar si la BD está en otro servidor
            user="root",  # Cambiar al usuario de la BD
            password="password",  # Cambiar a la contraseña de la BD
            database="restaurante_db"  # Nombre de la base de datos
        )

        # Crear cursor para ejecutar consultas
        cursor = conexion.cursor()
        return conexion, cursor
    except mysql.connector.Error as e:
        print("Error al conectar a la base de datos:", e)
        return None, None


def cerrar_bd(conexion, cursor):
    """
    Función para cerrar la conexión y el cursor de la base de datos.
    """
    if cursor:
        cursor.close()
    if conexion:
        conexion.close()


def mostrar_menu():
    """
    Muestra el menú principal de opciones de la aplicación de restaurante.
    """
    print("\n" + "=" * 50)
    print("    SISTEMA DE GESTIÓN DE RESTAURANTE  ")
    print("=" * 50)
    print("1. Crear una nueva reservación")
    print("2. Ver reservaciones existentes")
    print("3. Registrar un nuevo pedido")
    print("4. Ver pedidos existentes")
    print("5. Ver inventario de ingredientes")
    print("6. Salir de la aplicación")


def crear_reservacion():
    """
    Registra una nueva reservación en la tabla 'reservaciones'.
    """
    conexion, cursor = conectar_bd()

    if not conexion or not cursor:
        print("No se pudo conectar a la base de datos para crear una reservación.")
        return

    print("\nCreación de una nueva reservación:")
    nombre_cliente = input("Ingrese el nombre del cliente: ")
    fecha_reserva = input("Ingrese la fecha de la reservación (YYYY-MM-DD): ")
    hora_reserva = input("Ingrese la hora de la reservación (HH:MM:SS): ")
    mesa_id = input("Ingrese el número de mesa: ")

    # Insertar la reservación en la tabla 'reservaciones'
    sql = """
    INSERT INTO reservaciones (nombre_cliente, fecha_reserva, hora_reserva, mesa_id, estado)
    VALUES (%s, %s, %s, %s, 'Pendiente')
    """
    valores = (nombre_cliente, fecha_reserva, hora_reserva, mesa_id)

    try:
        cursor.execute(sql, valores)
        conexion.commit()
        print("Reservación creada exitosamente.")
    except mysql.connector.Error as e:
        print("Error al crear la reservación:", e)
        conexion.rollback()

    cerrar_bd(conexion, cursor)


def ver_reservaciones():
    """
    Muestra las reservaciones almacenadas en la tabla 'reservaciones'.
    """
    conexion, cursor = conectar_bd()
    if not conexion or not cursor:
        print("No se pudo conectar a la base de datos para ver las reservaciones.")
        return

    sql = "SELECT id_reserva, nombre_cliente, fecha_reserva, hora_reserva, mesa_id, estado FROM reservaciones"

    try:
        cursor.execute(sql)
        reservaciones = cursor.fetchall()

        if len(reservaciones) == 0:
            print("\nNo hay reservaciones registradas.")
        else: