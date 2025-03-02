create database EmpireLibrary;
use EmpireLibrary;
create table usuario(
id_usuario int auto_increment primary key,
nombre varchar(50),
rol varchar(20),
telefono varchar (15),
mail varchar(50),
direccion varchar(50),
contrasena varchar(255)
)

SELECT * from usuario;

INSERT INTO usuario (nombre, rol, telefono, mail, direccion, contrasena) VALUES
('Admin', 'Admin', '0000000000', 'admin@admin.com', 'admin', 'scrypt:32768:8:1$MuF28AmBUXUABGw4$ac657f1aa6d9c7a77cb851b6343da00d77d5462c84d1feffe4e5802c665b98edd3ced73a4c0337f96711b0ce71a8ffd8a8ab0d20b2e3c3b2b1a8e3c894026606'),
('Usuario', 'Usuario', '999999999', 'usuario@usuario.com', 'usuario', 'scrypt:32768:8:1$fRvdWlmIEFFOPQnw$8e108af2e3317242ebadf28f01430430bbe7a94ab3a99a0a5a3115de762ac990e60d352ddfe38c75d5de69d12fd61380a2d0e4e60bef926cd3d0e109e65d12f0'),


create table ventas(
id_ventas int auto_increment primary key,
vendido_a_clientes int(50),
totales_vendidos int(10),
FOREIGN KEY (vendido_a_clientes) REFERENCES usuario(id_usuario)
)


create table libros(
id_libro int auto_increment primary key,
nombre varchar(50),
autor varchar(50),
ano_publicacion int(10),
stock int(10),
genero varchar(30),
fecha_pub DATE,
estado varchar(20)
)

DESC libros;


alter table libros add COLUMN fecha_pub DATE;

ALTER TABLE libros 
MODIFY fecha_pub DATETIME DEFAULT CURRENT_TIMESTAMP;


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

CREATE TABLE ratings (
    id_rating INT AUTO_INCREMENT PRIMARY KEY,  -- ID único para cada rating
    idLibro INT,
    rating INT CHECK (rating BETWEEN 1 AND 5),  -- Asegura valores válidos (1-5)
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Guarda la fecha y hora del rating
    FOREIGN KEY (idLibro) REFERENCES libros(id_libro) ON DELETE CASCADE
);


drop table ratings;

INSERT INTO ratings (idLibro, rating) VALUES 
(1, 5), (2, 4), (3, 3), (4, 5), (5, 2), 
(1, 4), (2, 5), (3, 2), (4, 1), (5, 3), 
(6, 4), (7, 5), (8, 3), (9, 2), (10, 5), 
(6, 2), (7, 4), (8, 1), (9, 5), (10, 3);

SELECT AVG(rating)
FROM ratings
WHERE idLibro = 9;

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
CREATE PROCEDURE validateUser(
    IN p_mail VARCHAR(255)
    )
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
    IN p_ano_publicacion INT,
    IN p_stock INT,
    IN p_genero VARCHAR(30),
    IN p_fecha_pub DATE,
    IN p_estado VARCHAR(20)
)
BEGIN
    UPDATE libros
    SET nombre = p_nombre, 
        autor = p_autor, 
        ano_publicacion = p_ano_publicacion, 
        stock = p_stock, 
        genero = p_genero, 
        fecha_pub = p_fecha_pub, 
        estado = p_estado
    WHERE id_libro = p_id;
END //
DELIMITER ;

drop Procedure `updateLibro`

DELIMITER //
CREATE PROCEDURE deleteLibro(
    IN p_id INT
)
BEGIN
    DELETE FROM libros WHERE id_libro = p_id;
END //
DELIMITER ;

-- Procedimiento para actualizar los datos del usuario sin cambiar la contraseña
DELIMITER //
CREATE PROCEDURE actualizarUsuarioDatos(
    IN p_mail VARCHAR(100),
    IN p_nombre VARCHAR(100),
    IN p_direccion VARCHAR(255),
    IN p_telefono VARCHAR(20)
)
BEGIN
    UPDATE usuario
    SET nombre = p_nombre, 
        direccion = p_direccion, 
        telefono = p_telefono
    WHERE mail = p_mail;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE actualizarUsuarioCompleto(
    IN p_mail VARCHAR(100),
    IN p_nombre VARCHAR(100),
    IN p_direccion VARCHAR(255),
    IN p_telefono VARCHAR(20),
    IN p_contrasena VARCHAR(255)
)
BEGIN
    UPDATE usuario
    SET nombre = p_nombre, 
        direccion = p_direccion, 
        telefono = p_telefono, 
        contrasena = p_contrasena
    WHERE mail = p_mail;
END //
DELIMITER;

DELIMITER //

CREATE PROCEDURE listar_libros_con_ratings()
BEGIN
    SELECT l.id_libro, l.nombre, AVG(r.rating) AS promedio_rating
    FROM libros l
    LEFT JOIN ratings r ON l.id_libro = r.idLibro
    GROUP BY l.id_libro, l.nombre;
END //

DELIMITER;