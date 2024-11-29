
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