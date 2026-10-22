import mysql.connector

def obtener_conexion():
    try:
        return mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='db_academica',
            charset='utf8mb4'
        )
    except mysql.connector.Error as err:
        print(f"Error de conexión: {err}")
        return None