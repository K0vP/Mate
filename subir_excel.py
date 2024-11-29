import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def seleccionar_archivo():
    root = Tk()
    root.withdraw()

    archivo = askopenfilename(
        title="Selecciona el archivo Excel",
        filetypes=[("Archivos Excel", "*.xlsx;*.xlsm")]
    )
    return archivo

# Ejemplo de uso
archivo_seleccionado = seleccionar_archivo()

if archivo_seleccionado:
    print(f"Archivo seleccionado: {archivo_seleccionado}")
else:
    print("No se seleccionó ningún archivo.")
