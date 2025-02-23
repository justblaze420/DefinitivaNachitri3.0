create database EmpireLibrary;
use EmpireLibrary;
create table usuario(
id_usuario int auto_increment primary key,
nombre varchar(50),
rol varchar(20),
telefono varchar (15),
mail varchar(50),
direccion varchar(50),
contrasena varchar(50)
)

SELECT * from usuario;

INSERT INTO usuario (nombre, rol, telefono, mail, direccion, contrasena) VALUES
('Juan Pérez', 'Admin', '5551234567', 'juan.perez@example.com', 'Calle Falsa 123', 'juan123'),
('María López', 'Usuario', '5552345678', 'maria.lopez@example.com', 'Avenida Siempre Viva 456', 'maria456'),
('Carlos Sánchez', 'Usuario', '5553456789', 'carlos.sanchez@example.com', 'Boulevard de los Sueños Rotos 789', 'carlos789'),
('Ana Torres', 'Usuario', '5554567890', 'ana.torres@example.com', 'Calle Luna 101', 'ana101'),
('Luis Morales', 'Usuario', '5555678901', 'luis.morales@example.com', 'Avenida Sol 202', 'luis202'),
('Sofía Ramírez', 'Admin', '5556789012', 'sofia.ramirez@example.com', 'Calle Estrella 303', 'sofia303'),
('Pedro Gómez', 'Usuario', '5557890123', 'pedro.gomez@example.com', 'Avenida Libertad 404', 'pedro404'),
('Laura Díaz', 'Usuario', '5558901234', 'laura.diaz@example.com', 'Calle Esperanza 505', 'laura505'),
('Miguel Ruiz', 'Admin', '5559012345', 'miguel.ruiz@example.com', 'Boulevard Paz 606', 'miguel606'),
('Elena Castro', 'Usuario', '5550123456', 'elena.castro@example.com', 'Avenida Justicia 707', 'elena707');

create table ventas(
id_ventas int auto_increment primary key,
vendido_a_clientes int(50),
totales_vendidos int(10),
FOREIGN KEY (vendido_a_clientes) REFERENCES usuario(id_usuario)
)


create table libros(
id int auto_increment primary key,
nombre varchar(50),
autor varchar(50),
año_publicacion int(10),
stock int(10),
genero varchar(30),
estado varchar(20)
)

INSERT INTO libros (nombre, autor, año_publicacion, stock, genero, estado) VALUES
('Cien años de soledad', 'Gabriel García Márquez', 1967, 10, 'Realismo mágico', 'Disponible'),
('1984', 'George Orwell', 1949, 5, 'Ciencia ficción', 'Disponible'),
('El principito', 'Antoine de Saint-Exupéry', 1943, 15, 'Literatura infantil', 'Disponible'),
('Don Quijote de la Mancha', 'Miguel de Cervantes', 1605, 8, 'Novela clásica', 'Disponible'),
('Orgullo y prejuicio', 'Jane Austen', 1813, 12, 'Romance', 'Disponible'),
('Crimen y castigo', 'Fiódor Dostoyevski', 1866, 7, 'Novela psicológica', 'Disponible'),
('El señor de los anillos', 'J.R.R. Tolkien', 1954, 20, 'Fantasía', 'Disponible'),
('Harry Potter y la piedra filosofal', 'J.K. Rowling', 1997, 25, 'Fantasía', 'Disponible'),
('La sombra del viento', 'Carlos Ruiz Zafón', 2001, 9, 'Misterio', 'Disponible'),
('Los juegos del hambre', 'Suzanne Collins', 2008, 18, 'Ciencia ficción', 'Disponible'),
('El código Da Vinci', 'Dan Brown', 2003, 14, 'Thriller', 'Disponible'),
('Rayuela', 'Julio Cortázar', 1963, 6, 'Literatura experimental', 'Disponible'),
('Fahrenheit 451', 'Ray Bradbury', 1953, 11, 'Ciencia ficción', 'Disponible'),
('El retrato de Dorian Gray', 'Oscar Wilde', 1890, 13, 'Novela gótica', 'Disponible'),
('La metamorfosis', 'Franz Kafka', 1915, 4, 'Literatura filosófica', 'Disponible'),
('El hobbit', 'J.R.R. Tolkien', 1937, 22, 'Fantasía', 'Disponible'),
('Las crónicas de Narnia', 'C.S. Lewis', 1950, 17, 'Fantasía', 'Disponible'),
('El nombre del viento', 'Patrick Rothfuss', 2007, 10, 'Fantasía', 'Disponible'),
('Los pilares de la Tierra', 'Ken Follett', 1989, 8, 'Novela histórica', 'Disponible'),
('El alquimista', 'Paulo Coelho', 1988, 19, 'Ficción espiritual', 'Disponible');

select * from usuario;
select * from libros;
select * from ventas;
DELIMITER //
CREATE PROCEDURE GetAllUsers()
BEGIN
    SELECT * FROM usuario;
END //
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE insertUser(
    IN nombre VARCHAR(50),
    IN rol VARCHAR(50),
    IN telefono VARCHAR(50),
    IN mail VARCHAR(50),
    IN direccion VARCHAR(50),
    IN contrasena VARCHAR(255)
    )
BEGIN
    INSERT INTO usuario(nombre, rol, telefono, mail, direccion,contrasena) VALUES (nombre, rol, telefono, mail, direccion, contrasena);
END $$
DELIMITER ;

DELIMITER &&
CREATE PROCEDURE deleteUser(
    IN u_nombre VARCHAR(50),
    IN u_id_usuario INT
    )
BEGIN
    DELETE FROM usuario WHERE nombre = u_nombre AND id_usuario = u_id_usuario;
END &&
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE updateUser(
    IN p_id INT,
    IN p_nom VARCHAR(50),
    IN p_rol VARCHAR(50),
    IN p_tel VARCHAR(50),
    IN p_mail VARCHAR(50),
    IN p_add VARCHAR(50),
    IN p_pass VARCHAR(255)
)
BEGIN
    UPDATE usuario 
    SET nombre = p_nom, 
        rol = p_rol, 
        telefono = p_tel, 
        mail = p_mail, 
        direccion = p_add,
        contrasena = p_pass
    WHERE id_usuario = p_id;
END $$

DELIMITER ;

DELIMITER &&
CREATE PROCEDURE validateUser(IN p_mail VARCHAR(255))
BEGIN
    SELECT nombre, rol, telefono, mail, direccion, contrasena 
    FROM usuario
    WHERE mail = p_mail;
END //
DELIMITER ;

DROP Procedure `validateUser`

