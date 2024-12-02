import sys
sys.path.append('c:\\GitHub\\Mate\\src')
import sys
import tkinter as tk
from tkinter import messagebox, simpledialog
from src.DB.iniciar_db import inicializar_bd
from src.auth.autenticar import autenticar_usuario
from src.config.horarios import HORARIOS_VALIDOS
from src.service.crear import crear_turno
from src.service.asignar_turnos import asignar_horarios_optimizado
from export.exportar_excel import exportar_datos_excel
from export.exportar_pdf import exportar_datos_pdf
from src.visualizar.grafico import graficar_cumplimiento_horas

class MenuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Turnos")
        self.role = None

        # Inicializar la base de datos y autenticar usuario
        inicializar_bd()
        self.role = autenticar_usuario()
        if not self.role:
            messagebox.showerror("Error", "No se pudo autenticar al usuario.")
            self.root.destroy()
            return

        # Crear widgets
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.root, text="Seleccione una opción:")
        self.label.pack(pady=10)

        self.btn_crear_turno = tk.Button(self.root, text="Crear Turno Manual", command=self.crear_turno)
        self.btn_crear_turno.pack(pady=5)

        if self.role == "admin":
            self.btn_asignar_turnos = tk.Button(self.root, text="Asignar Turnos Automáticamente", command=self.asignar_turnos)
            self.btn_asignar_turnos.pack(pady=5)

            self.btn_exportar_datos = tk.Button(self.root, text="Exportar Datos", command=self.exportar_datos)
            self.btn_exportar_datos.pack(pady=5)

            self.btn_ver_estadisticas = tk.Button(self.root, text="Ver Estadísticas", command=self.ver_estadisticas)
            self.btn_ver_estadisticas.pack(pady=5)

        self.btn_salir = tk.Button(self.root, text="Salir", command=self.root.quit)
        self.btn_salir.pack(pady=20)

    def crear_turno(self):
        # Crear widgets para ingresar datos del turno
        self.clear_widgets()
        self.label.config(text="Crear Turno Manual")

        tk.Label(self.root, text="ID del empleado:").pack(pady=5)
        empleado_id_entry = tk.Entry(self.root)
        empleado_id_entry.pack(pady=5)

        tk.Label(self.root, text="Horario (opciones: {}):".format(HORARIOS_VALIDOS)).pack(pady=5)
        horario_entry = tk.Entry(self.root)
        horario_entry.pack(pady=5)

        tk.Label(self.root, text="Día (YYYY-MM-DD):").pack(pady=5)
        dia_entry = tk.Entry(self.root)
        dia_entry.pack(pady=5)

        tk.Label(self.root, text="Horas extras (máximo 2):").pack(pady=5)
        horas_extras_entry = tk.Entry(self.root)
        horas_extras_entry.pack(pady=5)

        def submit_turno():
            empleado_id = int(empleado_id_entry.get())
            horario = horario_entry.get()
            dia = dia_entry.get()
            horas_extras = int(horas_extras_entry.get() or 0)
            crear_turno(empleado_id, horario, dia, horas_extras)
            self.create_widgets()  # Regresar a la vista principal

        tk.Button(self.root, text="Crear Turno", command=submit_turno).pack(pady=10)

    def asignar_turnos(self):
        asignar_horarios_optimizado()
        messagebox.showinfo("Info", "Turnos asignados automáticamente.")
        self.create_widgets()  # Regresar a la vista principal

    def exportar_datos(self):
        formato = simpledialog.askstring("Formato a exportar", "Escriba el formato a exportar (excel / pdf):")
        if formato == "pdf":
            exportar_datos_pdf()
        elif formato == "excel":
            exportar_datos_excel()
        else:
            messagebox.showwarning("Advertencia", "Formato no válido.")
        self.create_widgets()  # Regresar a la vista principal

    def ver_estadisticas(self):
        graficar_cumplimiento_horas()
        self.create_widgets()  # Regresar a la vista principal

    def clear_widgets(self):
        for widget in self.root.winfo_children():
            widget

def menu_app():
    root = tk.Tk()
    app = MenuApp(root)
    root.mainloop()