CREATE DATABASE IF NOT EXISTS restaurante_db;
USE restaurante_db;

CREATE TABLE IF NOT EXISTS mesas (
    mesa_id INT AUTO_INCREMENT PRIMARY KEY,
    numero_mesa INT NOT NULL,
    ubicacion VARCHAR(100) NOT NULL,
    estado VARCHAR(20) NOT NULL DEFAULT 'Disponible'
);

CREATE TABLE IF NOT EXISTS reservaciones (
    id_reserva INT AUTO_INCREMENT PRIMARY KEY,
    nombre_cliente VARCHAR(100) NOT NULL,
    fecha_reserva DATE NOT NULL,
    hora_reserva TIME NOT NULL,
    mesa_id INT NOT NULL,
    estado VARCHAR(20) NOT NULL DEFAULT 'Pendiente',
    FOREIGN KEY (mesa_id) REFERENCES mesas(mesa_id)
);