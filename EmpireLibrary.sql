create database EmpireLibrary;
use EmpireLibrary;
create table usuario(
id_usuario int auto_increment primary key,
nombre varchar(20),
rol varchar(20),
telefono varchar (15),
mail varchar(30),
direccion varchar(50)
)

create table ventas(
id_ventas int auto_increment primary key,
vendido_a_clientes int(10),
totales_vendidos int(10),
FOREIGN KEY (vendido_a_clientes) REFERENCES usuario(id_usuario)
)

create table libros(
id int auto_increment primary key,
nombre varchar(50),
autor varchar(20),
año_publicacion int(10),
stock int(10),
genero varchar(30),
estado varchar(20)
)

show full tables from EmpireLibrary;

DESCRIBE ventas;

INSERT INTO usuario (nombre, rol, telefono, mail, direccion) VALUES
('Juan Perez', 'Admin', 5551234567, 'juan.perez@example.com', 'Calle Falsa 123'),
('Maria Lopez', 'Usuario', 5552345678, 'maria.lopez@example.com', 'Avenida Siempre Viva 456'),
('Carlos Sanchez', 'Usuario', 5553456789, 'carlos.sanchez@example.com', 'Boulevard de los Sueños Rotos 789'),
('Ana Torres', 'Usuario', 5554567890, 'ana.torres@example.com', 'Calle Luna 101'),
('Luis Morales', 'Usuario', 5555678901, 'luis.morales@example.com', 'Avenida Sol 202');

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
CREATE PROCEDURE insertUser1(
    IN nombre VARCHAR(50),
    IN rol VARCHAR(50),
    IN telefono VARCHAR(50),
    IN mail VARCHAR(50),
    IN direccion VARCHAR(50)
    )
BEGIN
    INSERT INTO usuario(nombre, rol, telefono, mail, direccion) VALUES (nombre, rol, telefono, mail, direccion);
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
    IN nombre VARCHAR(50),
    IN rol VARCHAR(50),
    IN telefono VARCHAR(50),
    IN mail VARCHAR(50),
    IN direccion VARCHAR(50),
    IN u_id_usuario INT
)
BEGIN
    UPDATE usuario
    SET nombre = nombre,
        rol = rol,
        telefono = telefono,
        mail = mail,
        direccion = direccion
    WHERE id_usuario = u_id_usuario;
END $$
DELIMITER ;