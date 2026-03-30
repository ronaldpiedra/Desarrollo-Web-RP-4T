import mysql.connector

def obtener_conexion():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="desarrollo_web_sem15",
        port=3307
    )
    return conexion