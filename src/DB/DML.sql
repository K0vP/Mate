-- Insertar datos iniciales en la tabla empleados
INSERT INTO empleados (nombre, rol) VALUES
('Juan Pérez', 'Cajero'),
('Ana López', 'Supervisora'),
('Carlos García', 'Reponedor');

-- Insertar datos iniciales en la tabla turnos
INSERT INTO turnos (empleado_id, horario, dia, horas_extras) VALUES
(1, '08:00-15:00', '2024-10-16', 1),
(2, '15:00-22:00', '2024-10-17', 0),
(3, '08:00-15:00', '2024-10-18', 2);

-- Insertar datos iniciales en la tabla solicitudes
INSERT INTO solicitudes (empleado_id, tipo_solicitud, detalles, estado) VALUES
(1, 'permiso', 'Permiso por asuntos personales', 'pendiente'),
(2, 'cambio', 'Cambio solicitado por necesidades personales', 'pendiente'),
(3, 'ausencia', 'Ausencia médica justificada', 'pendiente');