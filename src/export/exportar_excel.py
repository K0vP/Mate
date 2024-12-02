'''para exportar en Excel'''
import openpyxl
from tkinter import Tk
from tkinter.filedialog import asksaveasfilename
from src.DB.conexion_db import conectar_bd

def exportar_datos_excel():
    try:
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT e.nombre, t.horario, t.dia, t.horas_extras 
            FROM turnos t 
            JOIN empleados e ON t.empleado_id = e.id
        """)
        turnos = cursor.fetchall()

        # Crear un libro de trabajo y una hoja
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Turnos RRHH"

        # Escribir los encabezados
        sheet.append(["Empleado", "Horario", "Día", "Horas Extras"])

        # Escribir los datos
        for turno in turnos:
            sheet.append(turno)

        # Abrir un cuadro de diálogo para guardar el archivo
        Tk().withdraw()  # Ocultar la ventana principal de Tkinter
        file_path = asksaveasfilename(defaultextension=".xlsx", 
                                    filetypes=[("Archivos Excel", "*.xlsx;*.xlsm")],
                                    title="Guardar archivo como")
        if file_path:  # Si el usuario seleccionó una ruta
            workbook.save(file_path)
            print(f"Datos exportados a {file_path}")
        else:
            print("No se seleccionó ningún archivo.")
    except Exception as e:
        print(f"Error al exportar datos a Excel: {e}")
    finally:
        conn.close()