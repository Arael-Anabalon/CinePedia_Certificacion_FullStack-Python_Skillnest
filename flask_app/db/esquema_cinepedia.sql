-- Creación de DB para App flask "CinePedia"
CREATE DATABASE IF NOT EXISTS esquema_cinepedia; 
USE esquema_cinepedia; 

-- Tabla "usuarios"
CREATE TABLE IF NOT EXISTS usuarios ( 
    id_usuario INT AUTO_INCREMENT PRIMARY KEY, 
    nombre VARCHAR(100) NOT NULL, 
    apellido VARCHAR(100) NOT NULL, 
    email VARCHAR(200) NOT NULL, 
    contrasena VARCHAR(225) NOT NULL, 
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
    updated_at DATETIME NULL ON UPDATE CURRENT_TIMESTAMP, 
    created_by VARCHAR(50), 
    updated_by VARCHAR(50), 
    deleted TINYINT(1) NOT NULL DEFAULT 0, 
    CONSTRAINT uq_email UNIQUE (email) 
); 

-- Tabla "directores"
CREATE TABLE IF NOT EXISTS peliculas ( 
    id_pelicula INT AUTO_INCREMENT PRIMARY KEY, 
    titulo VARCHAR(100) NOT NULL UNIQUE, 
    director VARCHAR(100) NOT NULL, 
    fecha_estreno DATE NOT NULL, 
    sinopsis VARCHAR(500), 
    publicador_id INT NOT NULL, 
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
    updated_at DATETIME NULL ON UPDATE CURRENT_TIMESTAMP, 
    created_by VARCHAR(50), 
    updated_by VARCHAR(50), 
    deleted TINYINT(1) NOT NULL DEFAULT 0, 
    FOREIGN KEY (publicador_id) REFERENCES usuarios(id_usuario) ON DELETE CASCADE 
); 

-- Tabla "películas"
CREATE TABLE IF NOT EXISTS comentarios ( 
    id_comentario INT AUTO_INCREMENT PRIMARY KEY, 
    contenido VARCHAR(500) NOT NULL, 
    comentador_id INT NOT NULL, 
    pelicula_id INT NOT NULL, 
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
    updated_at DATETIME NULL ON UPDATE CURRENT_TIMESTAMP, 
    created_by VARCHAR(50), 
    updated_by VARCHAR(50), 
    deleted TINYINT(1) NOT NULL DEFAULT 0, 
    FOREIGN KEY (comentador_id) REFERENCES usuarios(id_usuario) ON DELETE CASCADE, 
    FOREIGN KEY (pelicula_id) REFERENCES peliculas(id_pelicula) ON DELETE CASCADE 
);
