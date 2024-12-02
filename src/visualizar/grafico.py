import matplotlib.pyplot as plt
from src.DB.conexion_db import conectar_bd
import io
import base64

def graficar_cumplimiento_horas():
    try:
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT e.nombre, SUM(TIMESTAMPDIFF(HOUR, 
                STR_TO_DATE(SUBSTRING_INDEX(t.horario, '-', 1), '%H:%i'), 
                STR_TO_DATE(SUBSTRING_INDEX(t.horario, '-', -1), '%H:%i')) + t.horas_extras) AS horas_totales
            FROM turnos t 
            JOIN empleados e ON t.empleado_id = e.id
            GROUP BY e.nombre
        """)
        datos = cursor.fetchall()

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

        # Guardar la imagen en un objeto BytesIO
        img = io.BytesIO()
        plt.savefig(img, format='png')
        plt.close()
        img.seek(0)
        # Codificar la imagen en base64
        img_base64 = base64.b64encode(img.getvalue()).decode('utf8')
        return img_base64
    except Exception as e:
        print(f"Error al graficar cumplimiento de horas: {e}")
        return None
    finally:
        conn.close()