-- Tabla de provincias
CREATE TABLE provincias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE
);

-- Tabla de ciudades
CREATE TABLE ciudades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    es_costera BOOLEAN NOT NULL,
    provincia_id INT NOT NULL,
    FOREIGN KEY (provincia_id) REFERENCES provincias(id)
);

-- Tabla de rutas
CREATE TABLE rutas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ciudad_origen_id INT NOT NULL,
    ciudad_destino_id INT NOT NULL,
    costo DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (ciudad_origen_id) REFERENCES ciudades(id),
    FOREIGN KEY (ciudad_destino_id) REFERENCES ciudades(id)
);

-- Insertar provincias
INSERT INTO provincias (nombre) VALUES
('Imbabura'),
('Pichincha'),
('Manabí'),
('Guayas'),
('Azuay'),
('Loja'),
('Santo Domingo de los Tsáchilas');

-- Insertar ciudades
INSERT INTO ciudades (nombre, es_costera, provincia_id) VALUES
('Ibarra', 0, (SELECT id FROM provincias WHERE nombre = 'Imbabura')),
('Quito', 0, (SELECT id FROM provincias WHERE nombre = 'Pichincha')),
('Santo Domingo', 0, (SELECT id FROM provincias WHERE nombre = 'Santo Domingo de los Tsáchilas')),
('Manta', 1, (SELECT id FROM provincias WHERE nombre = 'Manabí')),
('Portoviejo', 1, (SELECT id FROM provincias WHERE nombre = 'Manabí')),
('Guayaquil', 1, (SELECT id FROM provincias WHERE nombre = 'Guayas')),
('Cuenca', 0, (SELECT id FROM provincias WHERE nombre = 'Azuay')),
('Loja', 0, (SELECT id FROM provincias WHERE nombre = 'Loja'));

-- Insertar rutas
INSERT INTO rutas (ciudad_origen_id, ciudad_destino_id, costo) VALUES
((SELECT id FROM ciudades WHERE nombre = 'Ibarra'), (SELECT id FROM ciudades WHERE nombre = 'Quito'), 10),
((SELECT id FROM ciudades WHERE nombre = 'Quito'), (SELECT id FROM ciudades WHERE nombre = 'Santo Domingo'), 15),
((SELECT id FROM ciudades WHERE nombre = 'Quito'), (SELECT id FROM ciudades WHERE nombre = 'Manta'), 30),
((SELECT id FROM ciudades WHERE nombre = 'Santo Domingo'), (SELECT id FROM ciudades WHERE nombre = 'Manta'), 12),
((SELECT id FROM ciudades WHERE nombre = 'Manta'), (SELECT id FROM ciudades WHERE nombre = 'Portoviejo'), 5),
((SELECT id FROM ciudades WHERE nombre = 'Portoviejo'), (SELECT id FROM ciudades WHERE nombre = 'Guayaquil'), 20),
((SELECT id FROM ciudades WHERE nombre = 'Guayaquil'), (SELECT id FROM ciudades WHERE nombre = 'Cuenca'), 25),
((SELECT id FROM ciudades WHERE nombre = 'Cuenca'), (SELECT id FROM ciudades WHERE nombre = 'Loja'), 18),
((SELECT id FROM ciudades WHERE nombre = 'Quito'), (SELECT id FROM ciudades WHERE nombre = 'Cuenca'), 35),
((SELECT id FROM ciudades WHERE nombre = 'Santo Domingo'), (SELECT id FROM ciudades WHERE nombre = 'Guayaquil'), 22),
((SELECT id FROM ciudades WHERE nombre = 'Guayaquil'), (SELECT id FROM ciudades WHERE nombre = 'Loja'), 40);
