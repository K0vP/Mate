import mysql.connector
from datetime import datetime
import random
import pandas as pd
import matplotlib.pyplot as plt

# Conexión a la base de datos
def conectar_bd():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Cambia por tu usuario de MySQL
        password="tu_contraseña",  # Cambia por tu contraseña de MySQL
        database="worksync"
    )

# Inicializar la base de datos
def inicializar_bd():
    conn = conectar_bd()
    cursor = conn.cursor()

    # Crear las tablas si no existen
    cursor.execute('''CREATE TABLE IF NOT EXISTS empleados (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        nombre VARCHAR(255) NOT NULL,
                        rol VARCHAR(255) NOT NULL)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS turnos (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        empleado_id INT NOT NULL,
                        horario VARCHAR(255) NOT NULL,
                        dia DATE NOT NULL,
                        horas_extras INT DEFAULT 0,
                        FOREIGN KEY (empleado_id) REFERENCES empleados(id) ON DELETE CASCADE)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS solicitudes (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        empleado_id INT NOT NULL,
                        tipo_solicitud ENUM('cambio', 'permiso', 'ausencia'),
                        detalles TEXT,
                        estado ENUM('pendiente', 'aprobada', 'rechazada') DEFAULT 'pendiente',
                        FOREIGN KEY (empleado_id) REFERENCES empleados(id) ON DELETE CASCADE)''')

    conn.commit()
    conn.close()
    print("Base de datos inicializada.")

# Lista de horarios válidos
HORARIOS_VALIDOS = [
    "08:00-15:00",  # Turno de mañana con 1 hora de descanso
    "15:00-22:00"   # Turno de tarde con 1 hora de descanso
]

# Usuarios y roles
usuarios = {
    "admin": {"password": "1234", "role": "admin"},
    "empleado": {"password": "abcd", "role": "empleado"}
}

# Validar turno antes de asignarlo
def validar_turno(empleado_id, horario, dia, horas_extras=0):
    conn = conectar_bd()
    cursor = conn.cursor()

    # Validar domingos libres
    cursor.execute("""
        SELECT COUNT(*) 
        FROM turnos 
        WHERE empleado_id = %s 
        AND DAYNAME(dia) = 'Sunday'
        AND MONTH(dia) = MONTH(%s)
    """, (empleado_id, dia))
    domingos_asignados = cursor.fetchone()[0]

    if datetime.strptime(dia, "%Y-%m-%d").weekday() == 6 and domingos_asignados >= 2:
        print("El empleado ya tiene dos domingos asignados este mes.")
        conn.close()
        return False

    # Validar horas trabajadas (máximo 8 horas por día incluyendo extras)
    inicio, fin = horario.split("-")
    horas_turno = (datetime.strptime(fin, "%H:%M") - datetime.strptime(inicio, "%H:%M")).seconds / 3600

    if horas_turno + horas_extras > 8:
        print("No se pueden asignar más de 8 horas diarias (incluyendo extras).")
        conn.close()
        return False

    # Validar horas semanales
    cursor.execute("""
        SELECT SUM(TIMESTAMPDIFF(HOUR, 
            STR_TO_DATE(SUBSTRING_INDEX(horario, '-', 1), '%H:%i'), 
            STR_TO_DATE(SUBSTRING_INDEX(horario, '-', -1), '%H:%i')) + horas_extras)
        FROM turnos 
        WHERE empleado_id = %s 
        AND WEEK(dia) = WEEK(%s)
    """, (empleado_id, dia))
    horas_semanales = cursor.fetchone()[0] or 0

    if horas_semanales + horas_turno > 40:
        print(f"El empleado ya tiene {horas_semanales} horas asignadas esta semana. No puede exceder las 40 horas.")
        conn.close()
        return False

    conn.close()
    return True

# Crear turno manualmente con validaciones
def crear_turno(empleado_id, horario, dia, horas_extras=0):
    if validar_turno(empleado_id, horario, dia, horas_extras):
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO turnos (empleado_id, horario, dia, horas_extras) VALUES (%s, %s, %s, %s)",
                    (empleado_id, horario, dia, horas_extras))
        conn.commit()
        conn.close()
        print("Turno creado correctamente.")
    else:
        print("No se pudo crear el turno debido a restricciones.")

# # Asignar turnos automáticamente
# def asignar_horarios_optimizado():
#     conn = conectar_bd()
#     cursor = conn.cursor()

#     # Obtener empleados y fechas
#     cursor.execute("SELECT id, nombre FROM empleados")
#     empleados = cursor.fetchall()

#     dias = ["2024-10-16", "2024-10-17", "2024-10-18"]  # Ejemplo de fechas
#     horarios = HORARIOS_VALIDOS

#     # Asignar turnos respetando restricciones
#     for dia in dias:
#         for horario in horarios:
#             for empleado in empleados:
#                 if validar_turno(empleado[0], horario, dia):
#                     cursor.execute(
#                         "INSERT INTO turnos (empleado_id, horario, dia) VALUES (%s, %s, %s)",
#                         (empleado[0], horario, dia)
#                     )
#                     print(f"Turno asignado: {empleado[1]} - {horario} - {dia}")
#                     break  # Solo un turno por horario y día

#     conn.commit()
#     conn.close()

# Asignar turnos automáticamente
def asignar_horarios_optimizado():
    conn = conectar_bd()
    cursor = conn.cursor()

    # Obtener empleados y fechas
    cursor.execute("SELECT id, nombre FROM empleados")
    empleados = cursor.fetchall()

    dias = ["2024-10-16", "2024-10-17", "2024-10-18"]  # Ejemplo de fechas
    horarios = HORARIOS_VALIDOS

    # Asignar turnos respetando restricciones
    for dia in dias:
        for horario in horarios:
            for empleado in empleados:
                # Verificar si ya existe un turno para este empleado en el día
                cursor.execute("SELECT COUNT(*) FROM turnos WHERE empleado_id = %s AND dia = %s", (empleado[0], dia))
                turno_existente = cursor.fetchone()[0]

                if turno_existente > 0:
                    continue  # Si ya tiene un turno, pasar al siguiente empleado

                if validar_turno(empleado[0], horario, dia):
                    cursor.execute(
                        "INSERT INTO turnos (empleado_id, horario, dia) VALUES (%s, %s, %s)",
                        (empleado[0], horario, dia)
                    )
                    print(f"Turno asignado: {empleado[1]} - {horario} - {dia}")
                    break  # Solo un turno por horario y día

    conn.commit()
    conn.close()

# Exportar datos
def exportar_datos_csv():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT e.nombre, t.horario, t.dia, t.horas_extras FROM turnos t JOIN empleados e ON t.empleado_id = e.id")
    turnos = cursor.fetchall()
    conn.close()

    with open("turnos_rrhh.csv", "w") as f:
        f.write("Empleado,Horario,Día,Horas Extras\n")
        for turno in turnos:
            f.write(",".join(map(str, turno)) + "\n")
    print("Datos exportados a turnos_rrhh.csv")

# Gráficos de estadísticas
def graficar_cumplimiento_horas():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT e.nombre, SUM(TIMESTAMPDIFF(HOUR, 
            STR_TO_DATE(SUBSTRING_INDEX(t.horario, '-', 1), '%H:%i'), 
            STR_TO_DATE(SUBSTRING_INDEX(t.horario, '-', -1), '%H:%i')) + t.horas_extras) AS horas_totales
        FROM turnos t JOIN empleados e ON t.empleado_id = e.id
        GROUP BY e.nombre
    """)
    datos = cursor.fetchall()
    conn.close()

    # Extraer datos para el gráfico
    empleados = [d[0] for d in datos]
    horas_totales = [d[1] for d in datos]

    # Generar el gráfico
    plt.bar(empleados, horas_totales, color="blue")
    plt.axhline(40, color="red", linestyle="--", label="Máximo semanal")
    plt.title("Cumplimiento de Horas Semanales por Empleado")
    plt.xlabel("Empleados")
    plt.ylabel("Horas Totales")
    plt.legend()
    plt.savefig("cumplimiento_horas.png")
    plt.show()
    print("Gráfico generado: cumplimiento_horas.png")

# Autenticación de usuarios
def autenticar_usuario():
    username = input("Usuario: ")
    password = input("Contraseña: ")
    if username in usuarios and usuarios[username]["password"] == password:
        print(f"Bienvenido, {username} ({usuarios[username]['role']})")
        return usuarios[username]["role"]
    else:
        print("Usuario o contraseña incorrectos.")
        return None

# Menú principal
def menu_principal():
    inicializar_bd()
    role = autenticar_usuario()
    if not role:
        return

    while True:
        print("\n1. Crear turno manual")
        if role == "admin":
            print("2. Asignar turnos automáticamente")
            print("3. Exportar datos")
            print("4. Ver estadísticas")
        print("5. Salir")
        
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            empleado_id = int(input("ID del empleado: "))
            horario = input(f"Horario (opciones: {HORARIOS_VALIDOS}): ")
            dia = input("Día (YYYY-MM-DD): ")
            horas_extras = int(input("Horas extras (máximo 2): ") or 0)
            crear_turno(empleado_id, horario, dia, horas_extras)
        elif opcion == "2" and role == "admin":
            asignar_horarios_optimizado()
        elif opcion == "3" and role == "admin":
            exportar_datos_csv()
        elif opcion == "4" and role == "admin":
            graficar_cumplimiento_horas()
        elif opcion == "5":
            break
        else:
            print("Opción inválida.")

# Ejecutar el menú
if __name__ == "__main__":
    menu_principal()