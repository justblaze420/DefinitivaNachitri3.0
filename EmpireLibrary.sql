create database EmpireLibrary;
use EmpireLibrary;
create table usuario(
id_usuario int auto_increment primary key,
nombre varchar(50),
rol varchar(20),
telefono varchar (15),
mail varchar(50),
contrasena varchar(255)
)

INSERT INTO usuario (nombre, rol, telefono, mail, contrasena) VALUES
('Admin', 'Admin', '0000000000', 'admin@admin.com', 'scrypt:32768:8:1$MuF28AmBUXUABGw4$ac657f1aa6d9c7a77cb851b6343da00d77d5462c84d1feffe4e5802c665b98edd3ced73a4c0337f96711b0ce71a8ffd8a8ab0d20b2e3c3b2b1a8e3c894026606'),
('Usuario', 'Usuario', '999999999', 'usuario@usuario.com', 'scrypt:32768:8:1$fRvdWlmIEFFOPQnw$8e108af2e3317242ebadf28f01430430bbe7a94ab3a99a0a5a3115de762ac990e60d352ddfe38c75d5de69d12fd61380a2d0e4e60bef926cd3d0e109e65d12f0')


create table ventas(
id_ventas int auto_increment primary key,
vendido_a_clientes int(50),
totales_vendidos int(10),
FOREIGN KEY (vendido_a_clientes) REFERENCES usuario(id_usuario)
)

ALTER TABLE ventas 
ADD COLUMN fecha_venta DATETIME DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN total DECIMAL(10,2) DEFAULT 0.00,
ADD COLUMN estado VARCHAR(20) DEFAULT 'pendiente';

-- Crear tabla para detalles de ventas
CREATE TABLE venta_detalle (
    id_detalle INT AUTO_INCREMENT PRIMARY KEY,
    id_venta INT NOT NULL,
    id_libro INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_venta) REFERENCES ventas(id_ventas),
    FOREIGN KEY (id_libro) REFERENCES libros(id_libro)
);

create table libros(
id_libro int auto_increment primary key,
nombre varchar(50),
autor varchar(50),
ano_publicacion int(10),
stock int(10),
genero varchar(30),
fecha_pub DATETIME,
precio DECIMAL(10,2) NOT NULL,
estado varchar(20)
)

INSERT INTO libros (nombre, autor, ano_publicacion, stock, genero, fecha_pub, precio, estado) VALUES
('Matar un ruiseñor', 'Harper Lee', 1960, 8, 'Drama', '2024-03-18 10:00:00', 14.20, 'Disponible'),
('El Gran Gatsby', 'F. Scott Fitzgerald', 1925, 6, 'Clásico', '2024-03-18 10:00:00', 11.99, 'Disponible'),
('Crimen y castigo', 'Fiódor Dostoievski', 1866, 4, 'Psicológico', '2024-03-18 10:00:00', 16.50, 'Disponible'),
('Hamlet', 'William Shakespeare', 1603, 9, 'Tragedia', '2024-03-18 10:00:00', 9.75, 'Disponible'),
('El Señor de los Anillos', 'J.R.R. Tolkien', 1954, 12, 'Fantasía', '2024-03-18 10:00:00', 22.00, 'Disponible'),
('Los juegos del hambre', 'Suzanne Collins', 2008, 15, 'Ciencia Ficción', '2024-03-18 10:00:00', 13.40, 'Disponible'),
('El código Da Vinci', 'Dan Brown', 2003, 11, 'Thriller', '2024-03-18 10:00:00', 17.80, 'Disponible'),
('Las Crónicas de Narnia', 'C.S. Lewis', 1950, 7, 'Fantasía', '2024-03-18 10:00:00', 12.50, 'Disponible'),
('El alquimista', 'Paulo Coelho', 1988, 14, 'Fábula', '2024-03-18 10:00:00', 10.99, 'Disponible'),
('El Principito', 'Antoine de Saint-Exupéry', 1943, 10, 'Infantil', '2024-03-18 10:00:00', 8.00, 'Disponible');


ALTER TABLE libros ADD COLUMN precio DECIMAL(10,2) NOT NULL DEFAULT 0.00;

ALTER TABLE libros 
MODIFY fecha_pub DATETIME DEFAULT CURRENT_TIMESTAMP;

drop

CREATE TABLE ratings (
    id_rating INT AUTO_INCREMENT PRIMARY KEY,
    idLibro INT,
    idUsuario INT,
    comentario TEXT NOT NULL,
    rating INT CHECK (rating BETWEEN 1 AND 5),  
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    FOREIGN KEY (idLibro) REFERENCES libros(id_libro) ON DELETE CASCADE,
    FOREIGN KEY (idUsuario) REFERENCES usuario(id_usuario) ON DELETE CASCADE
);

INSERT INTO ratings (idLibro, idUsuario, comentario, rating) VALUES
(1, 14, '¡Un clásico imprescindible!', 5),
(2, 15, 'Me encantó la trama y los personajes.', 4),
(3, 16, 'Un libro que te hace reflexionar.', 5),
(4, 17, 'No pude parar de leerlo.', 4),
(5, 14, 'Una historia conmovedora.', 5),
(6, 14, 'Muy entretenido y fácil de leer.', 4),
(7, 17, 'Un thriller que te atrapa desde el principio.', 5),
(8, 16, 'Una aventura épica.', 4),
(9, 14, 'Un libro que te cambia la vida.', 5),
(10, 15, 'Una joya de la literatura infantil.', 5);

ALTER TABLE ratings ADD CONSTRAINT unique_user_book_rating UNIQUE (idLibro, idUsuario);

INSERT INTO ratings (idLibro, idUsuario, comentario, rating, fecha) VALUES
(1, 1, 'Una obra maestra de la literatura latinoamericana.', 5, '2023-06-10 14:30:00'),
(1, 2, 'Me costó entrar en la historia, pero el final es impresionante.', 4, '2023-06-15 09:45:00'),
(2, 3, 'Entretenido y adictivo, aunque algo predecible.', 3, '2023-06-20 18:20:00'),
(2, 4, 'Me encantó el ritmo y los enigmas.', 5, '2023-06-25 11:15:00'),
(3, 5, 'Una introducción perfecta al mundo mágico.', 5, '2023-07-01 16:40:00'),
(3, 1, 'Un clásico moderno para todas las edades.', 4, '2023-07-05 13:25:00'),
(4, 2, 'Escalofriante y más relevante que nunca.', 5, '2023-07-10 19:50:00'),
(5, 3, 'Sencillo pero profundo. Una joya.', 5, '2023-07-15 10:35:00'),
(5, 4, 'Cada relectura descubro algo nuevo.', 5, '2023-07-20 15:15:00'),
(4, 5, 'Una distopía brillante y aterradora.', 4, '2023-07-25 12:55:00');

CREATE TABLE carrito (
    id_carrito INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(20) DEFAULT 'activo',
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);

drop Table carrito

drop table carrito_items

CREATE TABLE carrito_items (
    id_item INT AUTO_INCREMENT PRIMARY KEY,
    id_carrito INT NOT NULL,
    id_libro INT NOT NULL,
    cantidad INT NOT NULL DEFAULT 1,
    precio_unitario DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_carrito) REFERENCES carrito(id_carrito),
    FOREIGN KEY (id_libro) REFERENCES libros(id_libro)
);


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
    IN contrasena VARCHAR(255)
    )
BEGIN
    INSERT INTO usuario(nombre, rol, telefono, mail,contrasena) VALUES (nombre, rol, telefono, mail, contrasena);
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
    IN p_pass VARCHAR(255)
)
BEGIN
    UPDATE usuario 
    SET nombre = p_nom, 
        rol = p_rol, 
        telefono = p_tel, 
        mail = p_mail, 
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
    SELECT id_usuario,nombre, rol, telefono, mail, contrasena 
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
    IN p_nombre VARCHAR(50),
    IN p_autor VARCHAR(50),
    IN p_ano_publicacion INT,
    IN p_stock INT,
    IN p_precio DECIMAL(10,2),
    IN p_genero VARCHAR(30),
    IN p_estado VARCHAR(20)
)
BEGIN
    INSERT INTO libros (nombre, autor, ano_publicacion, stock,precio, genero, fecha_pub, estado)
    VALUES (p_nombre, p_autor, p_ano_publicacion, p_stock, p_precio, p_genero, NOW(), p_estado);
END
DELIMITER ;

DELIMITER //
CREATE PROCEDURE updateLibro(
    IN p_id INT,
    IN p_nombre VARCHAR(50),
    IN p_autor VARCHAR(50),
    IN p_ano_publicacion INT,
    IN p_stock INT,
    IN p_precio DECIMAL(10,2),
    IN p_genero VARCHAR(30),
    IN p_fecha_pub DATETIME,
    IN p_estado VARCHAR(20)
)
BEGIN
    UPDATE libros
    SET nombre = p_nombre, 
        autor = p_autor, 
        ano_publicacion = p_ano_publicacion, 
        stock = p_stock, 
        precio = p_precio,
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

DELIMITER //
CREATE PROCEDURE actualizarUsuarioDatos(
    IN p_mail VARCHAR(100),
    IN p_nombre VARCHAR(100),
    IN p_telefono VARCHAR(20)
)
BEGIN
    UPDATE usuar    io
    SET nombre = p_nombre, 
        telefono = p_telefono
    WHERE mail = p_mail;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE actualizarUsuarioCompleto(
    IN p_mail VARCHAR(100),
    IN p_nombre VARCHAR(100),
    IN p_telefono VARCHAR(20),
    IN p_contrasena VARCHAR(255)
)
BEGIN
    UPDATE usuario
    SET nombre = p_nombre, 
        telefono = p_telefono, 
        contrasena = p_contrasena
    WHERE mail = p_mail;
END //
DELIMITER;


DELIMITER //


DELIMITER //
CREATE PROCEDURE listBookRatings()
BEGIN
    SELECT
        libros.id_libro,
        libros.nombre,
        IFNULL(AVG(ratings.rating), 0) AS promedio_rating,
        GROUP_CONCAT(ratings.rating SEPARATOR '||') AS ratings,
        GROUP_CONCAT(ratings.comentario SEPARATOR '||') AS comentarios,
        GROUP_CONCAT(usuario.nombre SEPARATOR '||') AS nombres_usuarios,
        GROUP_CONCAT(ratings.fecha SEPARATOR '||') AS fechas,
        GROUP_CONCAT(ratings.idUsuario SEPARATOR '||') AS ids_usuarios
    FROM libros
    LEFT JOIN ratings ON libros.id_libro = ratings.idLibro
    LEFT JOIN usuario ON ratings.idUsuario = usuario.id_usuario
    WHERE ratings.idLibro IS NOT NULL
    GROUP BY libros.id_libro;
END //
DELIMITER ;

-- Llamar al procedimiento almacenado
CALL listBookRatings();

DELIMITER //

CREATE PROCEDURE insertRating(
    IN p_idLibro INT,
    IN p_idUsuario INT,
    IN p_rating INT,
    IN p_comentario TEXT
)
BEGIN
    DECLARE v_ratingExists INT DEFAULT 0;
    
    -- Validar que el rating esté entre 1 y 5
    IF p_rating < 1 OR p_rating > 5 THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'El rating debe estar entre 1 y 5';
    END IF;
    
    -- Verificar si ya existe un rating para este usuario y libro
    SELECT COUNT(*) INTO v_ratingExists 
    FROM ratings 
    WHERE idLibro = p_idLibro AND idUsuario = p_idUsuario;
    
    -- Si ya existe, actualizar el registro existente
    IF v_ratingExists > 0 THEN
        UPDATE ratings 
        SET rating = p_rating, 
            comentario = p_comentario,
            fecha = CURRENT_TIMESTAMP 
        WHERE idLibro = p_idLibro AND idUsuario = p_idUsuario;
    -- Si no existe, insertar un nuevo registro
    ELSE
        INSERT INTO ratings (idLibro, idUsuario, rating, comentario) 
        VALUES (p_idLibro, p_idUsuario, p_rating, p_comentario);
    END IF;
    
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE sp_ver_carrito(IN p_id_usuario INT)
BEGIN
    -- Obtener el ID del carrito activo del usuario
    DECLARE v_id_carrito INT;
    
    SELECT id_carrito INTO v_id_carrito 
    FROM carrito 
    WHERE id_usuario = p_id_usuario AND estado = 'activo' 
    ORDER BY fecha_creacion DESC LIMIT 1;
    
    -- Si el usuario tiene un carrito activo, mostrar los items
    IF v_id_carrito IS NOT NULL THEN
        -- Seleccionamos la información necesaria para mostrar en el carrito
        -- Incluimos información de los libros para mostrar detalles
        SELECT 
            ci.id_item,
            ci.id_carrito,
            ci.id_libro,
            l.nombre AS titulo,  -- Cambiado de titulo a nombre
            l.autor,
            l.genero,            -- Agregado género
            l.ano_publicacion,   --      año de publicación
            ci.cantidad,
            ci.precio_unitario,
            (ci.cantidad * ci.precio_unitario) AS subtotal,
            l.stock              -- Agregado stock para validaciones del lado cliente
        FROM 
            carrito_items ci
        INNER JOIN 
            libros l ON ci.id_libro = l.id_libro
        WHERE 
            ci.id_carrito = v_id_carrito
        ORDER BY 
            ci.id_item;
    ELSE
        -- Si el usuario no tiene un carrito activo, devolver un conjunto vacío
        -- con la misma estructura para evitar errores en la aplicación
        SELECT 
            NULL AS id_item,
            NULL AS id_carrito,
            NULL AS id_libro,
            NULL AS titulo,
            NULL AS autor,
            NULL AS genero,
            NULL AS ano_publicacion,
            NULL AS cantidad,
            NULL AS precio_unitario,
            NULL AS subtotal,
            NULL AS stock
        WHERE 
            1 = 0; -- Condición falsa para que no devuelva registros
    END IF;
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE sp_realizar_compra(IN p_id_usuario INT)
BEGIN
    -- Variables para la transacción
    DECLARE v_id_carrito INT;
    DECLARE v_id_venta INT;
    DECLARE v_total DECIMAL(10,2) DEFAULT 0;
    DECLARE v_error BOOLEAN DEFAULT FALSE;
    DECLARE v_mensaje VARCHAR(255);
    
    -- Handler para controlar errores
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION 
    BEGIN
        SET v_error = TRUE;
        SET v_mensaje = 'Error durante el procesamiento de la compra';
        ROLLBACK;
    END;
    
    -- Iniciar transacción
    START TRANSACTION;
    
    -- 1. Obtener el ID del carrito activo del usuario
    SELECT id_carrito INTO v_id_carrito
    FROM carrito
    WHERE id_usuario = p_id_usuario AND estado = 'activo'
    ORDER BY fecha_creacion DESC LIMIT 1;
    
    IF v_id_carrito IS NULL THEN
        SET v_error = TRUE;
        SET v_mensaje = 'No tienes un carrito activo';
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = v_mensaje;
    END IF;
    
    -- 2. Verificar si hay stock suficiente para cada libro en el carrito
    IF EXISTS (
        SELECT ci.id_libro
        FROM carrito_items ci
        JOIN libros l ON ci.id_libro = l.id_libro
        WHERE ci.id_carrito = v_id_carrito AND ci.cantidad > l.stock
    ) THEN
        SET v_error = TRUE;
        SET v_mensaje = 'Stock insuficiente para uno o más libros';
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = v_mensaje;
    END IF;
    
    -- 3. Crear el registro en la tabla ventas
    INSERT INTO ventas (vendido_a_clientes, fecha_venta, estado)
    VALUES (p_id_usuario, NOW(), 'completada');
    
    SET v_id_venta = LAST_INSERT_ID();
    
    -- 4. Insertar detalles de la venta y calcular el total
    INSERT INTO venta_detalle (id_venta, id_libro, cantidad, precio_unitario)
    SELECT 
        v_id_venta,
        ci.id_libro,
        ci.cantidad,
        ci.precio_unitario
    FROM carrito_items ci
    WHERE ci.id_carrito = v_id_carrito;
    
    -- 5. Actualizar el stock de libros
    UPDATE libros l
    JOIN carrito_items ci ON l.id_libro = ci.id_libro
    SET l.stock = l.stock - ci.cantidad
    WHERE ci.id_carrito = v_id_carrito;
    
    -- 6. Calcular y actualizar el total de la venta
    SELECT SUM(cantidad * precio_unitario) INTO v_total
    FROM venta_detalle
    WHERE id_venta = v_id_venta;
    
    UPDATE ventas
    SET total = v_total, totales_vendidos = (
        SELECT SUM(cantidad)
        FROM venta_detalle
        WHERE id_venta = v_id_venta
    )
    WHERE id_ventas = v_id_venta;
    
    -- 7. Marcar el carrito como completado/procesado
    UPDATE carrito
    SET estado = 'completado'
    WHERE id_carrito = v_id_carrito;
    
    -- 8. Si no hubo errores, confirmar la transacción
    IF NOT v_error THEN
        COMMIT;
        SELECT 'Compra realizada con éxito' AS mensaje, v_id_venta AS id_venta, v_total AS total;
    END IF;
END //

DELIMITER ;

DELIMITER //

drop Procedure sp_leer_checkout

DELIMITER //

CREATE PROCEDURE sp_leer_checkout(IN p_id_usuario INT)
BEGIN
    DECLARE v_id_carrito INT;
    DECLARE v_total DECIMAL(10,2) DEFAULT 0;
    
    -- Obtener el ID del carrito activo del usuario
    SELECT id_carrito INTO v_id_carrito 
    FROM carrito 
    WHERE id_usuario = p_id_usuario AND estado = 'activo' 
    ORDER BY fecha_creacion DESC LIMIT 1;
    
    -- Si el usuario tiene un carrito activo, mostrar los items
    IF v_id_carrito IS NOT NULL THEN
        -- Información principal del carrito
        SELECT 
            ci.id_item,
            ci.id_carrito,
            p_id_usuario AS id_usuario,
            ci.id_libro,
            l.nombre,
            l.autor,
            l.precio,
            ci.cantidad,
            (ci.precio_unitario * ci.cantidad) AS subtotal
        FROM 
            carrito_items ci
        INNER JOIN 
            libros l ON ci.id_libro = l.id_libro
        WHERE 
            ci.id_carrito = v_id_carrito;
        
        -- Calcular y devolver el total en una consulta separada
        SELECT 
            SUM(ci.precio_unitario * ci.cantidad) AS total,
            COUNT(ci.id_item) AS num_items,
            v_id_carrito AS id_carrito,
            'activo' AS estado_carrito
        FROM 
            carrito_items ci
        WHERE 
            ci.id_carrito = v_id_carrito;
            
        -- Obtener información del usuario para el checkout
        
        SELECT
            u.nombre,
            u.telefono,
            u.mail
        FROM
            usuario u
        WHERE
            u.id_usuario = p_id_usuario;
    ELSE
        -- Si no hay carrito, devolver conjuntos vacíos para mantener la estructura
        -- Conjunto 1: Items del carrito
        SELECT 
            NULL AS id_item,
            NULL AS id_carrito,
            p_id_usuario AS id_usuario,
            NULL AS id_libro,
            NULL AS nombre,
            NULL AS autor,
            NULL AS precio,
            NULL AS cantidad,
            NULL AS subtotal
        WHERE 1=0;
        
        -- Conjunto 2: Total y resumen
        SELECT 
            0.00 AS total,
            0 AS num_items,
            NULL AS id_carrito,
            NULL AS estado_carrito;
            
        -- Conjunto 3: Información del usuario 
        SELECT
            u.nombre,
            u.telefono,
            u.mail
        FROM
            usuario u
        WHERE
            u.id_usuario = p_id_usuario;
    END IF;
END //

DELIMITER ;

DELIMITER ;

DELIMITER //

CREATE PROCEDURE sp_eliminar_del_carrito(
    IN p_id_usuario INT,
    IN p_id_libro INT
)
BEGIN
    DECLARE v_id_carrito INT;
    DECLARE v_id_item INT;
    DECLARE v_error BOOLEAN DEFAULT FALSE;
    DECLARE v_mensaje VARCHAR(255);
    
    -- Handler para controlar errores
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION 
    BEGIN
        SET v_error = TRUE;
        SET v_mensaje = 'Error al eliminar el libro del carrito';
        ROLLBACK;
    END;
    
    -- Iniciar transacción
    START TRANSACTION;
    
    -- Obtener el ID del carrito activo del usuario
    SELECT id_carrito INTO v_id_carrito
    FROM carrito
    WHERE id_usuario = p_id_usuario AND estado = 'activo'
    ORDER BY fecha_creacion DESC LIMIT 1;
    
    IF v_id_carrito IS NULL THEN
        SET v_error = TRUE;
        SET v_mensaje = 'No tienes un carrito activo';
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = v_mensaje;
    END IF;
    
    -- Obtener el ID del item a eliminar
    SELECT id_item INTO v_id_item
    FROM carrito_items
    WHERE id_carrito = v_id_carrito AND id_libro = p_id_libro
    LIMIT 1;
    
    IF v_id_item IS NULL THEN
        SET v_error = TRUE;
        SET v_mensaje = 'El libro no se encuentra en el carrito';
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = v_mensaje;
    END IF;
    
    -- Eliminar el item del carrito
    DELETE FROM carrito_items
    WHERE id_item = v_id_item;
    
    -- Verificar si el carrito quedó vacío
    IF NOT EXISTS (SELECT 1 FROM carrito_items WHERE id_carrito = v_id_carrito) THEN
        -- Opcionalmente, podrías eliminar el carrito o marcarlo como vacío
        -- En este caso solo registramos que está vacío
        UPDATE carrito
        SET estado = 'vacio'
        WHERE id_carrito = v_id_carrito;
    END IF;
    
    -- Si no hubo errores, confirmar la transacción
    IF NOT v_error THEN
        COMMIT;
        SELECT 'Libro eliminado del carrito con éxito' AS mensaje;
    END IF;
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE sp_procesar_pago(IN p_id_usuario INT)
BEGIN
    DECLARE v_id_carrito INT;
    DECLARE v_id_venta INT;
    DECLARE v_total DECIMAL(10,2) DEFAULT 0;
    DECLARE v_error BOOLEAN DEFAULT FALSE;
    DECLARE v_mensaje VARCHAR(255);
    
    -- Handler para controlar errores
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION 
    BEGIN
        SET v_error = TRUE;
        SET v_mensaje = 'Error durante el procesamiento del pago';
        ROLLBACK;
    END;
    
    -- Iniciar transacción
    START TRANSACTION;
    
    -- 1. Obtener el ID del carrito activo del usuario
    SELECT id_carrito INTO v_id_carrito
    FROM carrito
    WHERE id_usuario = p_id_usuario AND estado = 'activo'
    ORDER BY fecha_creacion DESC LIMIT 1;
    
    IF v_id_carrito IS NULL THEN
        SET v_error = TRUE;
        SET v_mensaje = 'No tienes un carrito activo';
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = v_mensaje;
    END IF;
    
    -- 2. Verificar si hay items en el carrito
    IF NOT EXISTS (SELECT 1 FROM carrito_items WHERE id_carrito = v_id_carrito) THEN
        SET v_error = TRUE;
        SET v_mensaje = 'No hay productos en el carrito';
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = v_mensaje;
    END IF;
    
    -- 3. Verificar stock suficiente para cada libro
    IF EXISTS (
        SELECT ci.id_libro
        FROM carrito_items ci
        JOIN libros l ON ci.id_libro = l.id_libro
        WHERE ci.id_carrito = v_id_carrito AND ci.cantidad > l.stock
    ) THEN
        -- Obtener información del libro sin stock suficiente
        SELECT l.id_libro, l.nombre, l.stock, ci.cantidad
        INTO @id_libro_sin_stock, @nombre_libro, @stock_disponible, @cantidad_solicitada
        FROM carrito_items ci
        JOIN libros l ON ci.id_libro = l.id_libro
        WHERE ci.id_carrito = v_id_carrito AND ci.cantidad > l.stock
        LIMIT 1;
        
        SET v_error = TRUE;
        SET v_mensaje = CONCAT('Stock insuficiente para el libro: ', @nombre_libro, 
                              ' (ID: ', @id_libro_sin_stock, 
                              '). Disponible: ', @stock_disponible, 
                              ', Solicitado: ', @cantidad_solicitada);
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = v_mensaje;
    END IF;
    
    -- 4. Crear registro en la tabla ventas
    INSERT INTO ventas (vendido_a_clientes, fecha_venta, estado)
    VALUES (p_id_usuario, NOW(), 'completada');
    
    SET v_id_venta = LAST_INSERT_ID();
    
    -- 5. Insertar detalles de la venta
    INSERT INTO venta_detalle (id_venta, id_libro, cantidad, precio_unitario)
    SELECT 
        v_id_venta,
        ci.id_libro,
        ci.cantidad,
        ci.precio_unitario
    FROM carrito_items ci
    WHERE ci.id_carrito = v_id_carrito;
    
    -- 6. Actualizar el stock de libros
    UPDATE libros l
    JOIN carrito_items ci ON l.id_libro = ci.id_libro
    SET l.stock = l.stock - ci.cantidad
    WHERE ci.id_carrito = v_id_carrito;
    
    -- 7. Calcular y actualizar el total de la venta
    SELECT SUM(cantidad * precio_unitario) INTO v_total
    FROM venta_detalle
    WHERE id_venta = v_id_venta;
    
    UPDATE ventas
    SET total = v_total, totales_vendidos = (
        SELECT SUM(cantidad)
        FROM venta_detalle
        WHERE id_venta = v_id_venta
    )
    WHERE id_ventas = v_id_venta;
    
    -- 8. Marcar el carrito como completado
    UPDATE carrito
    SET estado = 'completado'
    WHERE id_carrito = v_id_carrito;
    
    -- 9. Si no hubo errores, confirmar la transacción
    IF NOT v_error THEN
        COMMIT;
        SELECT 'Pago procesado correctamente. ¡Gracias por tu compra!' AS mensaje, 
               v_id_venta AS id_venta, 
               v_total AS total;
    END IF;
END //

DELIMITER ;