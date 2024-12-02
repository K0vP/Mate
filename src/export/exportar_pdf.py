import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import table
from tkinter import Tk
from tkinter.filedialog import asksaveasfilename
from src.DB.conexion_db import conectar_bd

def exportar_datos_pdf():
    try:
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT e.nombre, t.horario, t.dia, t.horas_extras 
            FROM turnos t 
            JOIN empleados e ON t.empleado_id = e.id
        """)
        turnos = cursor.fetchall()

        # Crear un DataFrame de pandas
        df = pd.DataFrame(turnos, columns=["Empleado", "Horario", "Día", "Horas Extras"])

        # Crear una figura y un eje
        fig, ax = plt.subplots(figsize=(8, 4))  # Ajusta el tamaño según sea necesario
        ax.axis('tight')
        ax.axis('off')
        tabla = table(ax, df, loc='center', cellLoc='center', colWidths=[0.2]*len(df.columns))

        # Abrir un cuadro de diálogo para guardar el archivo
        Tk().withdraw()  # Ocultar la ventana principal de Tkinter
        file_path = asksaveasfilename(defaultextension=".pdf", 
                                    filetypes=[("Archivos PDF", "*.pdf")],
                                    title="Guardar archivo como")
        if file_path:  # Si el usuario seleccionó una ruta
            plt.savefig(file_path, bbox_inches='tight')
            plt.close(fig)
            print(f"Datos exportados a {file_path}")
        else:
            print("No se seleccionó ningún archivo.")
    except Exception as e:
        print(f"Error al exportar datos a PDF: {e}")
    finally:
        conn.close()