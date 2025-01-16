import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',         # Cambia esto por la IP de tu servidor
        user='root',        # Tu usuario de la base de datos
        password='', # Tu contraseña de la base de datos
        database='Proyecto_Final'      # El nombre de tu base de datos
    )
    return connection