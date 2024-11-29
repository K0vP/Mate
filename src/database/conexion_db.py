import mysql.connector
def conectar_bd():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="tu_contraseña",
        database="worksync"
    )