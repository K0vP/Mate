# def inicializar_bd():
#     from src.database.conexion_db import conectar_bd
#     conn = conectar_bd
#     cursor = conn.cursor()

#     cursor.execute('''CREATE TABLE IF NOT EXISTS empleados (
#                         id INT AUTO_INCREMENT PRIMARY KEY,
#                         nombre VARCHAR(255) NOT NULL,
#                         rol VARCHAR(255) NOT NULL)''')

#     cursor.execute('''CREATE TABLE IF NOT EXISTS turnos (
#                         id INT AUTO_INCREMENT PRIMARY KEY,
#                         empleado_id INT NOT NULL,
#                         horario VARCHAR(255) NOT NULL,
#                         dia DATE NOT NULL,
#                         horas_extras INT DEFAULT 0,
#                         FOREIGN KEY (empleado_id) REFERENCES empleados(id) ON DELETE CASCADE)''')

#     cursor.execute('''CREATE TABLE IF NOT EXISTS solicitudes (
#                         id INT AUTO_INCREMENT PRIMARY KEY,
#                         empleado_id INT NOT NULL,
#                         tipo_solicitud ENUM('cambio', 'permiso', 'ausencia'),
#                         detalles TEXT,
#                         estado ENUM('pendiente', 'aprobada', 'rechazada') DEFAULT 'pendiente',
#                         FOREIGN KEY (empleado_id) REFERENCES empleados(id) ON DELETE CASCADE)''')

#     conn.commit()
#     conn.close()
#     print("Base de datos inicializada.")

from src.DB.conexion_db import conectar_bd

def inicializar_bd():
    try:
        conn = conectar_bd()
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS empleados (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(255) NOT NULL,
                rol VARCHAR(255) NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS turnos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                empleado_id INT NOT NULL,
                horario VARCHAR(255) NOT NULL,
                dia DATE NOT NULL,
                horas_extras INT DEFAULT 0,
                FOREIGN KEY (empleado_id) REFERENCES empleados(id) ON DELETE CASCADE
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS solicitudes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                empleado_id INT NOT NULL,
                tipo_solicitud ENUM('cambio', 'permiso', 'ausencia'),
                detalles TEXT,
                estado ENUM('pendiente', 'aprobada', 'rechazada') DEFAULT 'pendiente',
                FOREIGN KEY (empleado_id) REFERENCES empleados(id) ON DELETE CASCADE
            )
        ''')

        conn.commit()
        print("Base de datos inicializada.")
    except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")
    finally:
        conn.close()