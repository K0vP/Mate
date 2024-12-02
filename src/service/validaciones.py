# def validar_turno(empleado_id, horario, dia, horas_extras=0):
#     from database.conexion_db import conectar_bd
#     from datetime import datetime
#     conn = conectar_bd()
#     cursor = conn.cursor()

#     # Validar domingos libres
#     cursor.execute("""
#         SELECT COUNT(*) 
#         FROM turnos 
#         WHERE empleado_id = %s 
#         AND DAYNAME(dia) = 'Sunday'
#         AND MONTH(dia) = MONTH(%s)
#     """, (empleado_id, dia))
#     domingos_asignados = cursor.fetchone()[0]

#     if datetime.strptime(dia, "%Y-%m-%d").weekday() == 6 and domingos_asignados >= 2:
#         print("El empleado ya tiene dos domingos asignados este mes.")
#         conn.close()
#         return False

#     # Validar horas trabajadas (máximo 8 horas por día incluyendo extras)
#     inicio, fin = horario.split("-")
#     horas_turno = (datetime.strptime(fin, "%H:%M") - datetime.strptime(inicio, "%H:%M")).seconds / 3600

#     if horas_turno + horas_extras > 8:
#         print("No se pueden asignar más de 8 horas diarias (incluyendo extras).")
#         conn.close()
#         return False

#     # Validar horas semanales
#     cursor.execute("""
#         SELECT SUM(TIMESTAMPDIFF(HOUR, 
#             STR_TO_DATE(SUBSTRING_INDEX(horario, '-', 1), '%H:%i'), 
#             STR_TO_DATE(SUBSTRING_INDEX(horario, '-', -1), '%H:%i')) + horas_extras)
#         FROM turnos 
#         WHERE empleado_id = %s 
#         AND WEEK(dia) = WEEK(%s)
#     """, (empleado_id, dia))
#     horas_semanales = cursor.fetchone()[0] or 0

#     if horas_semanales + horas_turno > 40:
#         print(f"El empleado ya tiene {horas_semanales} horas asignadas esta semana. No puede exceder las 40 horas.")
#         conn.close()
#         return False

#     conn.close()
#     return True

from DB.conexion_db import conectar_bd
from datetime import datetime

def validar_turno(empleado_id, horario, dia, horas_extras=0):
    try:
        conn = conectar_bd()
        with conn.cursor() as cursor:
            if not validar_domingos(cursor, empleado_id, dia):
                return False

            if not validar_horas_diarias(horario, horas_extras):
                return False

            if not validar_horas_semanales(cursor, empleado_id, horario, dia, horas_extras):
                return False

        return True
    except Exception as e:
        print(f"Error en la validación del turno: {e}")
        return False
    finally:
        conn.close()

def validar_domingos(cursor, empleado_id, dia):
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
        return False
    return True

def validar_horas_diarias(horario, horas_extras):
    horas_totales = calcular_horas(horario) + horas_extras
    if horas_totales > 8:
        print("El total de horas diarias no puede exceder las 8 horas.")
        return False
    return True

def validar_horas_semanales(cursor, empleado_id, horario, dia, horas_extras):
    cursor.execute("""
        SELECT SUM(horas_extras) + COUNT(*) * %s 
        FROM turnos 
        WHERE empleado_id = %s 
        AND WEEK(dia) = WEEK(%s)
    """, (calcular_horas(horario), empleado_id, dia))
    horas_semanales = cursor.fetchone()[0]
    
    if horas_semanales > 40:
        print("El empleado ya ha alcanzado el límite de horas semanales.")
        return False
    return True

def calcular_horas(horario):
    # Suponiendo que el horario es una cadena en formato "HH:MM-HH:MM"
    inicio, fin = horario.split('-')
    inicio_dt = datetime.strptime(inicio, "%H:%M")
    fin_dt = datetime.strptime(fin, "%H:%M")
    return (fin_dt - inicio_dt).seconds / 3600  # Convertir a horas