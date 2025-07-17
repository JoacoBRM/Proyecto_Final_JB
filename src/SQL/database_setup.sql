-- Script para crear la base de datos del proyecto
-- Base de datos: proyecto_final

-- Crear la base de datos si no existe
CREATE DATABASE IF NOT EXISTS proyecto_final;

-- Usar la base de datos creada
USE proyecto_final;

-- Crear tabla de usuarios
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    INDEX idx_username (username),
    INDEX idx_email (email)
);

-- Insertar un usuario de prueba (contraseña: 123456)
INSERT INTO users (username, email, password_hash) VALUES 
('admin', 'admin@proyecto_final_jb.com', '123456')
ON DUPLICATE KEY UPDATE id=id;

-- Mostrar las tablas creadas
SHOW TABLES;

-- Mostrar la estructura de la tabla users
DESCRIBE users;

-- Mostrar los datos de la tabla users
SELECT id, username, email, created_at, is_active FROM users;
