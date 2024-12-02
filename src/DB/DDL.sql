-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS worksync;

-- Usar la base de datos
USE worksync;

-- Crear la tabla de empleados
CREATE TABLE IF NOT EXISTS empleados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    rol VARCHAR(255) NOT NULL
);

-- Crear la tabla de turnos
CREATE TABLE IF NOT EXISTS turnos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    empleado_id INT NOT NULL,
    horario VARCHAR(255) NOT NULL,
    dia DATE NOT NULL,
    horas_extras INT DEFAULT 0,
    FOREIGN KEY (empleado_id) REFERENCES empleados(id) ON DELETE CASCADE
);

-- Crear la tabla de solicitudes
CREATE TABLE IF NOT EXISTS solicitudes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    empleado_id INT NOT NULL,
    tipo_solicitud ENUM('cambio', 'permiso', 'ausencia'),
    detalles TEXT,
    estado ENUM('pendiente', 'aprobada', 'rechazada') DEFAULT 'pendiente',
    FOREIGN KEY (empleado_id) REFERENCES empleados(id) ON DELETE CASCADE
);