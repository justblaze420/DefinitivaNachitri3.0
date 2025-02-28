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
ano_publicacion int(10),
stock int(10),
genero varchar(30),
fecha_pub DATE,
estado varchar(20)
)

alter table libros add COLUMN fecha_pub DATE;

INSERT INTO libros (nombre, autor, ano_publicacion, stock, genero, fecha_pub, estado) VALUES
('Cien años de soledad', 'Gabriel García Márquez', 1967, 10, 'Realismo mágico', '2024-01-15', 'Disponible'),
('1984', 'George Orwell', 1949, 5, 'Distopía', '2023-11-10', 'Disponible'),
('El Principito', 'Antoine de Saint-Exupéry', 1943, 15, 'Ficción', '2024-02-05', 'Disponible'),
('Don Quijote de la Mancha', 'Miguel de Cervantes', 1605, 3, 'Clásico', '2023-09-20', 'Agotado'),
('Harry Potter y la piedra filosofal', 'J.K. Rowling', 1997, 8, 'Fantasía', '2024-01-30', 'Disponible'),
('Crimen y castigo', 'Fiódor Dostoyevski', 1866, 6, 'Novela', '2023-12-12', 'Disponible'),
('Los juegos del hambre', 'Suzanne Collins', 2008, 12, 'Ciencia ficción', '2024-02-10', 'Disponible'),
('El código Da Vinci', 'Dan Brown', 2003, 7, 'Thriller', '2023-10-05', 'Disponible'),
('It', 'Stephen King', 1986, 4, 'Terror', '2024-01-25', 'Disponible'),
('Orgullo y prejuicio', 'Jane Austen', 1813, 9, 'Romance', '2023-11-18', 'Disponible');


drop table libros

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

drop Procedure `updateUser`

DELIMITER ;

DELIMITER &&
CREATE PROCEDURE validateUser(IN p_mail VARCHAR(255))
BEGIN
    SELECT nombre, rol, telefono, mail, direccion, contrasena 
    FROM usuario
    WHERE mail = p_mail;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE GetAllBooks()
BEGIN
    SELECT * FROM libros;
END //
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE insertBook(
    IN nombre VARCHAR(50),
    IN autor VARCHAR(50),
    IN ano_publicacion VARCHAR(50),
    IN stock INT(10),
    IN genero VARCHAR(50),
    IN fecha_pub DATE,
    IN estado VARCHAR(255)
    )
BEGIN
     INSERT INTO libros (nombre, autor, ano_publicacion, stock, genero, fecha_pub, estado)VALUES(nombre, autor, ano_publicacion, stock, genero, fecha_pub, estado);
END $$
DELIMITER ;

DELIMITER //
CREATE PROCEDURE updateLibro(
    IN p_id INT,
    IN p_nombre VARCHAR(50),
    IN p_autor VARCHAR(50),
    IN p_año_publicacion INT,
    IN p_stock INT,
    IN p_genero VARCHAR(30),
    IN p_fecha_pub DATE,
    IN p_estado VARCHAR(20)
)
BEGIN
    UPDATE libros
    SET nombre = p_nombre, 
        autor = p_autor, 
        año_publicacion = p_año_publicacion, 
        stock = p_stock, 
        genero = p_genero, 
        fecha_pub = p_fecha_pub, 
        estado = p_estado
    WHERE id = p_id;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE deleteLibro(
    IN p_nombre VARCHAR(50),
    IN p_id INT
)
BEGIN
    DELETE FROM libros
    WHERE nombre = p_nombre AND id = p_id;
END //
DELIMITER ;

DROP Procedure 

