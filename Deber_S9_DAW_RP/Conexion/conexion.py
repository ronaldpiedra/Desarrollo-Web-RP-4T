import mysql.connector

def obtener_conexion():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="proyecto_s13",
        port=3307
    )
    return conexion