# def crear_turno(empleado_id, horario, dia, horas_extras=0):
#     from service.validaciones import validar_turno
#     from src.database.conexion_db import conectar_bd
#     if validar_turno(empleado_id, horario, dia, horas_extras):
#         conn = conectar_bd()
#         cursor = conn.cursor()
#         cursor.execute("INSERT INTO turnos (empleado_id, horario, dia, horas_extras) VALUES (%s, %s, %s, %s)",
#                     (empleado_id, horario, dia, horas_extras))
#         conn.commit()
#         conn.close()
#         print("Turno creado correctamente.")
#     else:
#         print("No se pudo crear el turno debido a restricciones.")
from service.validaciones import validar_turno
from src.DB.conexion_db import conectar_bd

def crear_turno(empleado_id, horario, dia, horas_extras=0):
    if not validar_turno(empleado_id, horario, dia, horas_extras):
        print("No se pudo crear el turno debido a restricciones.")
        return

    try:
        conn = conectar_bd()
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO turnos (empleado_id, horario, dia, horas_extras) VALUES (%s, %s, %s, %s)",
                (empleado_id, horario, dia, horas_extras)
            )
        conn.commit()
        print("Turno creado correctamente.")
    except Exception as e:
        print(f"Error al crear el turno: {e}")
    finally:
        conn.close()