# def asignar_horarios_optimizado():
#     from src.database.conexion_db import conectar_bd
#     from src.config.horarios import HORARIOS_VALIDOS
#     from src.service.validaciones import validar_turno
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
#                 # Verificar si ya existe un turno para este empleado en el día
#                 cursor.execute("SELECT COUNT(*) FROM turnos WHERE empleado_id = %s AND dia = %s", (empleado[0], dia))
#                 turno_existente = cursor.fetchone()[0]

#                 if turno_existente > 0:
#                     continue  # Si ya tiene un turno, pasar al siguiente empleado

#                 if validar_turno(empleado[0], horario, dia):
#                     cursor.execute(
#                         "INSERT INTO turnos (empleado_id, horario, dia) VALUES (%s, %s, %s)",
#                         (empleado[0], horario, dia)
#                     )
#                     print(f"Turno asignado: {empleado[1]} - {horario} - {dia}")
#                     break  # Solo un turno por horario y día

#     conn.commit()
#     conn.close()
from src.DB.conexion_db import conectar_bd
from src.config.horarios import HORARIOS_VALIDOS
from src.service.validaciones import validar_turno

def asignar_horarios_optimizado():
    try:
        conn = conectar_bd()
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, nombre FROM empleados")
            empleados = cursor.fetchall()

            dias = ["2024-10-16", "2024-10-17", "2024-10-18"]
            for dia in dias:
                for horario in HORARIOS_VALIDOS:
                    for empleado in empleados:
                        cursor.execute(
                            "SELECT COUNT(*) FROM turnos WHERE empleado_id = %s AND dia = %s",
                            (empleado[0], dia)
                        )
                        if cursor.fetchone()[0] > 0:
                            continue

                        if validar_turno(empleado[0], horario, dia):
                            cursor.execute(
                                "INSERT INTO turnos (empleado_id, horario, dia) VALUES (%s, %s, %s)",
                                (empleado[0], horario, dia)
                            )
                            print(f"Turno asignado: {empleado[1]} - {horario} - {dia}")
                            break

        conn.commit()
    except Exception as e:
        print(f"Error al asignar turnos: {e}")
    finally:
        conn.close()