from flask import Flask, render_template, request, redirect, url_for, flash
from src.service.crear import crear_turno
from src.service.asignar_turnos import asignar_horarios_optimizado
from src.export.exportar_excel import exportar_datos_excel
from src.export.exportar_pdf import exportar_datos_pdf
from src.visualizar.grafico import graficar_cumplimiento_horas
from src.auth.autenticar import autenticar_usuario

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Cambia esto por una clave secreta más segura

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/menu', methods=['GET', 'POST'])
def menu():
    role = autenticar_usuario()
    if role is None:
        flash("No se pudo autenticar al usuario.")
        return redirect(url_for('index'))

    if request.method == 'POST':
        if 'crear_turno' in request.form:
            empleado_id = request.form['empleado_id']
            horario = request.form['horario']
            dia = request.form['dia']
            horas_extras = request.form['horas_extras']
            crear_turno(empleado_id, horario, dia, horas_extras)
            flash("Turno creado correctamente.")
        elif 'asignar_turnos' in request.form and role == "admin":
            asignar_horarios_optimizado()
            flash("Turnos asignados automáticamente.")
        elif 'exportar_excel' in request.form and role == "admin":
            exportar_datos_excel()
        elif 'exportar_pdf' in request.form and role == "admin":
            exportar_datos_pdf()
        elif 'ver_estadisticas' in request.form and role == "admin":
            graficar_cumplimiento_horas()
    return render_template('menu.html', role=role)

@app.route('/ver_estadisticas', methods=['GET', 'POST'])
def ver_estadisticas():
    role = autenticar_usuario()
    if role is None:
        flash("No se pudo autenticar al usuario.")
        return redirect(url_for('index'))

    img_base64 = None
    if request.method == 'POST':
        img_base64 = graficar_cumplimiento_horas()
    
    return render_template('ver_estadisticas.html', img_base64=img_base64, role=role)

if __name__ == '__main__':
    app.run(debug=True)