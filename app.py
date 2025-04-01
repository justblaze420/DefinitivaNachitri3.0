from connection_db import get_db_connection, secret_key, correoConfirmacion, init_mail
from flask import Flask, jsonify, render_template, request, flash, redirect, url_for, session
import mysql.connector 
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import yaml
import paypalrestsdk

app = Flask(__name__)
app.secret_key = secret_key()
app.permanent_session_lifetime = timedelta(days=7)  # Expira después de 30 minutos de inactividad
init_mail(app)


paypalrestsdk.configure({
  "mode": "sandbox", 
  "client_id": "ARru0Hz2NyklIJYv6_oODvFGf-E9X4tpqrXZoofYBlzauBt8RQ7amAhYpKgWl6ohSvzU3yHc8XSTGpWL",
  "client_secret": "EJi8zhgcyayb099eOLGT_yTWHXfnI59MsAYZ0Q3l-km0f4lwGejLErqtVsnWeFg4P6H9PW4rf_uBgYwR" })

# Función para cargar YAML
def load_buttons():
    with open("buttons.yaml", "r", encoding="utf-8") as file:
        return yaml.safe_load(file)
    
# Función para guardar cambios en YAML
def save_buttons(config):
    with open("buttons.yaml", "w", encoding="utf-8") as file:
        yaml.dump(config, file, default_flow_style=False, allow_unicode=True)

@app.route('/editButtons', methods=['GET'])
def editButtons():
    if 'rol' not in session or session['rol'] != 'Admin':
        flash("No tienes permisos para acceder a esta página.", "error")
        return redirect(url_for('indexPage'))
    
    buttons_config = load_buttons()
    return render_template('bottoms.html', buttons_config=buttons_config)

@app.route('/update_buttons', methods=['POST'])
def update_buttons():
    if 'rol' not in session or session['rol'] != 'Admin':
        flash("No tienes permisos para realizar esta acción.", "error")
        return redirect(url_for('indexPage'))

    buttons_config = load_buttons()

    for role in buttons_config['roles']:
        for i, button in enumerate(buttons_config['roles'][role]['buttons']):
            button['text'] = request.form.get(f"{role}_text_{i}")
            button['url'] = request.form.get(f"{role}_url_{i}")
            button['class'] = request.form.get(f"{role}_class_{i}")

    save_buttons(buttons_config)
    flash("Botones actualizados correctamente.", "success")
    
    return redirect(url_for('editButtons'))

@app.before_request
def make_session_permanent():
    session.permanent = True 
#redirige a la pagina que muestra los usuarios
@app.route('/usuarios')
def showUsers():
    return render_template('showUsers.html')

@app.route('/confimation')
def confirmation():
    if not session.get('user_id'):
        flash("Debes iniciar sesión para ver esta página.", "warning")
        return redirect(url_for('loginPage'))
    return render_template('confirmation.html', id_venta=request.args.get('id_venta'))

@app.route('/checkout')
def readCheckout():
    id_usuario = session.get('user_id')  # Verificamos si el usuario está logueado
    if not id_usuario:
        flash('Debes iniciar sesión para ver tu carrito.', 'warning')
        return redirect(url_for('loginPage'))
    
    id_usuario = session.get('user_id')
   
    if not id_usuario:
        flash("Debes iniciar sesión para realizar la compra.", "warning")
        return redirect(url_for('loginPage'))
   
    conexion = get_db_connection()
    cursor = conexion.cursor()
    
    # Llamar al stored procedure
    cursor.callproc('sp_leer_checkout', (id_usuario,))
    
    # Procesar los resultados
    resultados = list(cursor.stored_results())
    
    if resultados and len(resultados) >= 3:
        # Primer resultado: items del carrito
        carrito = resultados[0].fetchall()
        
        # Segundo resultado: total y resumen
        resumen = resultados[1].fetchone()
        total = resumen[0] if resumen else 0.00
        num_items = resumen[1] if resumen else 0

        

        # Tercer resultado: información del usuario (nombre, teléfono, etc.)
        info_usuario = resultados[2].fetchone()
    else:
        carrito = []
        total = 0.00
        num_items = 0
        info_usuario = None
  
    print("Carrito:", carrito)
    print("Resumen:", resumen)
    print("Info Usuario:", info_usuario)


    cursor.close()
    conexion.close()
    
    return render_template('checkout.html', 
                          carrito=carrito, 
                          total=total,
                          num_items=num_items,
                          info_usuario=info_usuario)

@app.route('/indexPage')
def indexPage():
    if 'mail' not in session:
        flash("Debes iniciar sesión para acceder a esta página.", "error")
        return redirect(url_for('loginPage'))
    
    buttons_config = load_buttons()
    options = buttons_config["roles"].get(session['rol'], buttons_config["roles"]["User"])

    return render_template('indexPage.html', nombre=session['nombre'], options=options)

@app.route('/logout')
def logout():
    session.clear()
    flash("Sesión cerrada exitosamente.", "success")
    return redirect(url_for('loginPage'))

@app.route('/cart', methods=['GET'])
def cart():
    id_usuario = session.get('user_id')  # Verificamos si el usuario está logueado
    if not id_usuario:
        flash('Debes iniciar sesión para ver tu carrito.', 'warning')
        return redirect(url_for('loginPage'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.callproc('sp_ver_carrito', (id_usuario,))  

    carrito = []
    for res in cursor.stored_results():
        carrito = res.fetchall()  # Obtenemos los libros en el carrito

    cursor.close()
    conn.close()

    return render_template('cart.html', carrito=carrito)

# redirige al index de la pagina despues de validar las credenciales
@app.route('/', methods=['GET', 'POST'])
def loginPage():
    if request.method == 'POST':
        mail = request.form.get('mail')
        passwd = request.form.get('contrasena')

        if not mail or not passwd:
            flash("Todos los datos deben ser ingresados", "error")
            return render_template('login.html')

        conn = None
        cursor = None  

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.callproc('validateUser', [mail])

            user = next(cursor.stored_results(), None).fetchone() if cursor.stored_results() else None

            if user and check_password_hash(user['contrasena'], passwd):
                flash("Inicio de sesión exitoso", "success")
                
                session.clear()  
                session.permanent = True
                
                session.update({
                    'user_id': user['id_usuario'],
                    'mail': user['mail'],
                    'nombre': user['nombre'],
                    'rol': user['rol'],
                    'telefono': user['telefono']
                })
                
                return redirect(url_for('indexPage'))
            else:
                flash("Email o contraseña incorrectos", "error")

        except mysql.connector.Error as error:
            flash(f"Error en el inicio de sesión: {error}", "error")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    return render_template('login.html')

#Creacion de usuarios
@app.route('/createUsers',methods=['GET','POST'])
def createUsers():
    nombre = request.form['nombre']
    rol = request.form['rol']
    telefono = request.form['telefono']
    mail = request.form['mail']
    contrasena = request.form['contrasena']
    
    if not nombre or not rol or not telefono or not mail or not contrasena:
        flash("Todos los campos son obligatorios.", "error")
        return redirect(url_for('readUsers'))
    
    hashed_password = generate_password_hash(contrasena)
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.callproc('insertUser', [nombre, rol, telefono, mail, hashed_password]) 
        conn.commit()
          
        flash("Usuario registrado correctamente.", "success")
    
    except mysql.connector.Error as error:
        flash(f"Error al registrar el usuario: {error}", "error")
    
    finally:
        cursor.close()  
        conn.close()
    
    return redirect(url_for('readUsers'))

#Funcion que muestra a los usuarios
@app.route('/readUsers',methods=['GET'])
def readUsers():
    id_usuario = session.get('user_id')  # Verificamos si el usuario está logueado
    if not id_usuario:
        flash('Debes iniciar sesión para ver tu carrito.', 'warning')
        return redirect(url_for('loginPage'))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    usuarios = [] 
    try:
        cursor.callproc('GetAllUsers')
        print("Procedimiento llamado exitosamente") 
        
        results = cursor.stored_results()
        print("Obteniendo resultados")
        
        for result in results:
            usuarios = result.fetchall() 

    except mysql.connector.Error as error:
        print(f"Error MySQL: {error}")  
        flash(f"Error al obtener los usuarios: {error}", "error")
        usuarios = []

    finally:
        cursor.close()
        conn.close()
    print(usuarios)
    return render_template('/showUsers.html', usuarios = usuarios)

#Funcion para elimina los users
@app.route('/deleteUsers', methods=['POST'])
def deleteUsers():
    nombre = request.form['nombre']
    id_usuario = request.form['id_usuario']
    
    if not nombre or not id_usuario:
        flash("Todos los campos son obligatorios.", "error")
        return redirect(url_for('readUsers'))

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.callproc('deleteUser', [nombre, id_usuario]) 
        conn.commit()
          
        flash("Usuario eliminado correctamente.", "success")
    except mysql.connector.Error as error:
        flash(f"Error al eliminar el usuario: {error}", "error")
    finally:
        cursor.close()  
        conn.close()

    return redirect(url_for('readUsers'))

#Funcion para actualizar los users
@app.route('/updateUsers', methods=['GET','POST'])
def updateUsers():
    user_id = request.form['id']
    nombre = request.form['nombre']
    rol = request.form['rol']
    telefono = request.form['telefono']
    mail = request.form['mail']
    contrasena = request.form['contrasena']
        
    if not nombre or not rol or not telefono or not mail:
        flash("Todos los campos son obligatorios.", "error")
        return redirect(url_for('readUsers'))
    
    hashed_password = generate_password_hash(contrasena)
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.callproc('updateUser', [user_id, nombre, rol, telefono, mail, hashed_password])
 
        conn.commit()
          
        flash("Usuario actualizado correctamente.", "success")
    
    except mysql.connector.Error as error:
        flash(f"Error al actualizado el usuario: {error}", "error")
    
    finally:
        cursor.close()  
        conn.close()
    
    return redirect(url_for('readUsers'))

#libros(nombre, autor, ano_publicacion, stock, genero, fecha_pub, estado)
@app.route('/createBook', methods=['GET', 'POST'])
def createBook():
    nombre = request.form['nombre']
    autor = request.form['autor']
    año_publicacion = request.form['ano_publicacion']
    stock = request.form['stock']
    precio = request.form['precio']
    genero = request.form['genero']
    estado = request.form['estado']
    
    if not nombre or not autor or not año_publicacion or not stock or not precio or not genero or not estado:
        flash("Todos los campos son obligatorios.", "error")
        return redirect(url_for('readBooks'))
    
    try:
        año_publicacion = int(año_publicacion)
        stock = int(stock)
        
    except ValueError:
        flash("Año de publicación y stock deben ser números válidos.", "error")
        return redirect(url_for('readBooks'))

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.callproc('insertBook', [nombre, autor, año_publicacion, stock, precio, genero, estado])
        conn.commit()
        flash("Libro registrado correctamente.", "success")
    
    except mysql.connector.Error as error:
        flash(f"Error al registrar el libro: {error}", "error")
    
    finally:
        cursor.close()  
        conn.close()
    
    return redirect(url_for('readBooks'))

@app.route('/readBooks', methods=['GET'])
def readBooks():    
    id_usuario = session.get('user_id')  # Verificamos si el usuario está logueado
    if not id_usuario:
        flash('Debes iniciar sesión para ver tu carrito.', 'warning')
        return redirect(url_for('loginPage'))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    libros = []
    ahora = datetime.now() 
    
    try:
        cursor.callproc('GetAllBooks')
        print("Procedimiento llamado exitosamente") 
        
        results = cursor.stored_results()
        print("Obteniendo resultados")
        
        for result in results:
            libros = result.fetchall() 
        
        for libro in libros:
            if libro['fecha_pub']:  
                # Asegúrate de que el formato coincida con 'YYYY-MM-DD HH:MM:SS'
                libro['fecha_pub'] = datetime.strptime(str(libro['fecha_pub']), '%Y-%m-%d %H:%M:%S')
                # Verifica si el libro es nuevo (menos de 24 horas desde su publicación)
                libro['es_nuevo'] = (ahora - libro['fecha_pub']) < timedelta(hours=24)
        
    except mysql.connector.Error as error:
        print(f"Error MySQL: {error}")  
        flash(f"Error al obtener los libros: {error}", "error")
        libros = []

    finally:
        cursor.close()
        conn.close()
    
    print(libros)
    return render_template('/showBooks.html', libros=libros)

@app.route('/deleteBook', methods=['POST'])
def deleteBooks():
    id_libro = request.form.get('id_libro')

    if not id_libro or not id_libro.isdigit():
        flash("El ID del libro es obligatorio y debe ser un número válido.", "error")
        return redirect(url_for('readBooks'))

    try:
        conn = get_db_connection()
        with conn.cursor(dictionary=True) as cursor:
            print(id_libro)
            cursor.callproc('deleteLibro', [int(id_libro)]) 
            conn.commit()

        flash("Libro eliminado correctamente.", "success")
    except mysql.connector.Error as error:
        flash(f"Error al eliminar el libro: {error}", "error")
    finally:
        conn.close()

    return redirect(url_for('readBooks'))

@app.route('/updateBook', methods=['POST'])
def updateBook():
    nombre = request.form.get('nombre')
    autor = request.form.get('autor')
    año_publicacion = request.form.get('ano_publicacion')
    stock = request.form.get('stock')
    precio = request.form.get('precio')
    genero = request.form.get('genero')
    fecha_pub = request.form.get('fecha_pub')
    estado = request.form.get('estado')
    id_libro = request.form.get('id')

    if not all([nombre, autor, año_publicacion, stock, precio, genero, fecha_pub, estado, id_libro]):
        flash("Todos los campos son obligatorios.", "error")
        return redirect(url_for('readBooks'))

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.callproc('updateLibro', [id_libro, nombre, autor, año_publicacion, stock, precio, genero, fecha_pub, estado])
        conn.commit()
        flash("Libro actualizado correctamente.", "success")
    except mysql.connector.Error as error:
        flash(f"Error al actualizar el libro: {error}", "error")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

    return redirect(url_for('readBooks'))

@app.route('/userConfig', methods=['GET','POST'])
def userConfig():
    id_usuario = session.get('user_id')  # Verificamos si el usuario está logueado
    if not id_usuario:
        flash('Debes iniciar sesión para ver tu carrito.', 'warning')
        return redirect(url_for('loginPage'))

    if 'mail' not in session:
        flash("Debe iniciar sesión primero", "error")
        return redirect(url_for('loginPage'))
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        telefono = request.form.get('telefono')
        contrasena_actual = request.form.get('contrasena_actual')
        nueva_contrasena = request.form.get('nueva_contrasena')
        confirmar_contrasena = request.form.get('confirmar_contrasena')
        
        conn = None
        cursor = None
        
        try:
            if not nombre or not telefono:
                flash("Nombre y teléfono son obligatorios", "error")
                return redirect(url_for('userConfig'))
            
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Si el usuario quiere cambiar la contraseña
            if contrasena_actual and nueva_contrasena and confirmar_contrasena:
                # Verificar que la contraseña actual sea correcta
                if not check_password_hash(session['contrasena'], contrasena_actual):
                    flash("La contraseña actual es incorrecta", "error")
                    return redirect(url_for('userConfig'))
                
                # Verificar que las nuevas contraseñas coincidan
                if nueva_contrasena != confirmar_contrasena:
                    flash("Las nuevas contraseñas no coinciden", "error")
                    return redirect(url_for('userConfig'))
                
                # Generar hash de la nueva contraseña
                hashed_password = generate_password_hash(nueva_contrasena)
                
                # Actualizar todos los datos incluyendo la contraseña
                cursor.callproc('actualizarUsuarioCompleto', [
                    session['mail'], 
                    nombre, 
                    telefono, 
                    hashed_password
                ])
                
                # Actualizar la sesión con la nueva contraseña
                session['contrasena'] = hashed_password
                
            else:
                # Actualizar solo los datos personales sin cambiar la contraseña
                cursor.callproc('actualizarUsuarioDatos', [
                    session['mail'], 
                    nombre, 
                    telefono
                ])
            
            conn.commit()
            
            session['nombre'] = nombre
            session['telefono'] = telefono
            
            flash("Datos actualizados correctamente", "success")
            return redirect(url_for('userConfig'))
            
        except mysql.connector.Error as error:
            flash(f"Error al actualizar los datos: {error}", "error")
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    return render_template('userConfig.html', 
                          nombre=session.get('nombre', ''),
                          telefono=session.get('telefono', ''),
                          mail=session.get('mail', ''))

@app.route('/bookRatings')
def bookRatings():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
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
            GROUP BY libros.id_libro
        """)
        
        libros = cursor.fetchall()
        
        # ID del usuario actual
        current_user_id = session.get('user_id')
        
        for libro in libros:
            # Inicializamos listas vacías para evitar errores
            libro['comentarios_list'] = []
            libro['nombres_usuarios_list'] = []
            libro['fechas_list'] = []
            libro['ratings_list'] = []
            libro['ids_usuarios_list'] = []
            
            # Verificamos si hay comentarios
            if libro['comentarios']:
                # Separamos los comentarios, nombres, fechas, ratings e ids_usuarios
                libro['comentarios_list'] = libro['comentarios'].split('||')
                libro['nombres_usuarios_list'] = libro['nombres_usuarios'].split('||') if libro['nombres_usuarios'] else ['Anónimo'] * len(libro['comentarios_list'])
                libro['fechas_list'] = libro['fechas'].split('||') if libro['fechas'] else ['0000-00-00 00:00:00'] * len(libro['comentarios_list'])
                libro['ratings_list'] = libro['ratings'].split('||') if libro['ratings'] else ['0'] * len(libro['comentarios_list'])
                libro['ids_usuarios_list'] = libro['ids_usuarios'].split('||') if libro['ids_usuarios'] else ['0'] * len(libro['comentarios_list'])
                
                # Creamos una lista de diccionarios para cada comentario
                libro['comentarios'] = []
                for i in range(len(libro['comentarios_list'])):
                    comentario_dict = {
                        'comentario': libro['comentarios_list'][i],
                        'usuario': libro['nombres_usuarios_list'][i] if i < len(libro['nombres_usuarios_list']) else 'Anónimo',
                        'fecha': libro['fechas_list'][i] if i < len(libro['fechas_list']) else '0000-00-00 00:00:00',
                        'rating': libro['ratings_list'][i] if i < len(libro['ratings_list']) else '0',
                        'id_usuario': libro['ids_usuarios_list'][i] if i < len(libro['ids_usuarios_list']) else '0',
                        'es_propio': str(libro['ids_usuarios_list'][i]) == str(current_user_id) if i < len(libro['ids_usuarios_list']) else False
                    }
                    libro['comentarios'].append(comentario_dict)
        
        return render_template('bookRatings.html', libros=libros, current_user_id=current_user_id)
    except mysql.connector.Error as error:
        flash(f"Error al obtener los ratings: {error}", "error")
        return redirect(url_for('indexPage'))
    finally:
        cursor.close()
        conn.close()
    
@app.route('/bookRating', methods=['POST'])
def bookRating():
    id_libro = request.form['id_libro']
    rating = request.form['rating']
    comentario = request.form['comentario']
    id_usuario = session.get('user_id')
    
    # Verificar que el ID de usuario existe en la sesión
    if not id_usuario:
        flash("Debe iniciar sesión para dejar un rating.", "error")
        return redirect(url_for('loginPage'))  
    
    try:
        rating = int(rating)
        if rating < 1 or rating > 5:
            flash("El rating debe estar entre 1 y 5.", "error")
            return redirect(url_for('bookRatings'))
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Imprimir para depuración
        print(f"ID Libro: {id_libro}, ID Usuario: {id_usuario}, Rating: {rating}")
        
        # Llamar al procedimiento almacenado
        cursor.callproc('insertRating', (id_libro, id_usuario, rating, comentario))
        
        conn.commit()
        flash("Rating guardado con éxito.", "success")
        
    except mysql.connector.Error as error:
        flash(f"Error al guardar el rating: {error}", "error")
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('bookRatings'))

@app.route('/addToCart', methods=['POST'])
def addToCart():
    id_usuario = session.get('user_id')  # Verifica si el usuario está logueado
    if not id_usuario:
        flash('Debes iniciar sesión para agregar libros al carrito.', 'warning')
        return redirect(url_for('loginPage'))
    
    # Obtener datos del formulario
    id_libro = request.form.get('id_libro')
    cantidad = int(request.form.get('cantidad', 1))

    if not id_libro:
        flash('Error al agregar el libro al carrito.', 'danger')
        return redirect(url_for('cart'))

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Verificar si el usuario ya tiene un carrito activo
        cursor.execute("SELECT id_carrito FROM carrito WHERE id_usuario = %s AND estado = 'activo'", (id_usuario,))
        carrito = cursor.fetchone()

        if not carrito:
            # Si no tiene carrito activo, crear uno
            cursor.execute("INSERT INTO carrito (id_usuario) VALUES (%s)", (id_usuario,))
            conn.commit()
            id_carrito = cursor.lastrowid
        else:
            id_carrito = carrito[0]

        # Obtener precio del libro
        cursor.execute("SELECT precio FROM libros WHERE id_libro = %s", (id_libro,))
        libro = cursor.fetchone()

        if not libro:
            flash('El libro no existe.', 'danger')
            return redirect(url_for('cart'))

        precio_unitario = libro[0]

        cursor.execute("SELECT id_item, cantidad FROM carrito_items WHERE id_carrito = %s AND id_libro = %s", (id_carrito, id_libro))
        item = cursor.fetchone()

        if item:
            nueva_cantidad = item[1] + cantidad
            cursor.execute("UPDATE carrito_items SET cantidad = %s WHERE id_item = %s", (nueva_cantidad, item[0]))
        else:
            cursor.execute(
                "INSERT INTO carrito_items (id_carrito, id_libro, cantidad, precio_unitario) VALUES (%s, %s, %s, %s)",
                (id_carrito, id_libro, cantidad, precio_unitario)
            )

        conn.commit()
        flash('Libro agregado al carrito.', 'success')

    except Exception as e:
        conn.rollback()
        flash(f'Error: {str(e)}', 'danger')
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('cart'))

@app.route('/checkout', methods=['POST'])
def checkoutProcedur():
    id_usuario = session.get('user_id')  # Verificamos si el usuario está logueado
    if not id_usuario:
        flash('Debes iniciar sesión para ver tu carrito.', 'warning')
        return redirect(url_for('loginPage'))
    
    id_usuario = session.get('user_id')
    if not id_usuario:
        flash('Debes iniciar sesión para realizar la compra.', 'warning')
        return redirect(url_for('loginPage'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.callproc('sp_realizar_compra', (id_usuario,))
        
        # Obtener el resultado del SP
        for result in cursor.stored_results():
            resultado = result.fetchone()
        
        conn.commit()
        mensaje = resultado[0]  # 'Compra realizada con éxito'
        id_venta = resultado[1]  # ID de la venta creada
        total = resultado[2]    # Total de la venta
        
        flash(f'{mensaje}. Total: ${total:.2f}', 'success')
        
    except Exception as e:
        conn.rollback()
        flash(f'Ocurrió un error al procesar la compra: {str(e)}', 'danger')
    finally:
        cursor.close()
        conn.close()
    
    return redirect(url_for('cart'))

@app.route('/removeFromCart', methods=['GET','POST'])
def removeFromCart():
    id_usuario = session.get('user_id')
    if not id_usuario:
        flash('Debes iniciar sesión para modificar el carrito.', 'warning')
        return redirect(url_for('loginPage'))
    
    id_libro = request.form.get('id_libro')
    if not id_libro:
        flash('No se proporcionó un libro para eliminar.', 'danger')
        return redirect(url_for('cart'))
    
    conexion = get_db_connection()
    cursor = conexion.cursor()
    
    try:
        cursor.callproc('sp_eliminar_del_carrito', (id_usuario, id_libro))
        
        for result in cursor.stored_results():
            mensaje = result.fetchone()[0]
        
        conexion.commit()
        flash(mensaje, 'success')
        
    except mysql.connector.Error as e:
        conexion.rollback()
        flash(f'Ocurrió un error al eliminar el libro: {str(e)}', 'danger')
    finally:
        cursor.close()
        conexion.close()
    
    return redirect(url_for('cart'))

@app.route('/payment', methods=['POST'])
def payProcedure():
    correo_usuario = session.get('mail')
    id_usuario = session.get('user_id')

    if not id_usuario or not correo_usuario:
        flash('Debes iniciar sesión para realizar la compra.', 'warning')
        return redirect(url_for('loginPage'))
        
    conexion = get_db_connection()
    cursor = conexion.cursor()

    try:

        cursor.callproc('sp_procesar_pago', (id_usuario,))

        # Obtener el resultado
        resultado = None
        for result in cursor.stored_results():
            resultado = result.fetchone()           

        # Verificar si resultado tiene datos
        if resultado:
            mensaje, id_venta, total = resultado  
            conexion.commit()

            # Enviar correo de confirmación
            correoConfirmacion(correo_usuario, id_venta, total)

            flash(f'{mensaje} Total: ${total:.2f}', 'success')
            return redirect(url_for('confirmation', id_venta=id_venta))
        
    except mysql.connector.Error as e:
        conexion.rollback()
        flash(f'Error al procesar el pago: {str(e)}', 'danger')

    finally:
        cursor.close()
        conexion.close()

    return redirect(url_for('cart'))

@app.route('/create_payment', methods=['POST'])
def create_payment():
    correo_usuario = session.get('mail')
    id_usuario = session.get('user_id')

    if not id_usuario or not correo_usuario:
        flash('Debes iniciar sesión para realizar la compra.', 'warning')
        return redirect(url_for('loginPage'))

    conexion = get_db_connection()
    cursor = conexion.cursor()

    try:
        cursor.callproc('sp_procesar_pago', (id_usuario,))
        
        resultado = None
        for result in cursor.stored_results():
            resultado = result.fetchone()  

        if resultado:
            mensaje, id_venta, total = resultado  
            conexion.commit()
            
            payment = paypalrestsdk.Payment({
                "intent": "sale",
                "payer": {
                    "payment_method": "paypal"
                },
                "redirect_urls": {
                    "return_url": url_for('execute_payment', id_venta=id_venta, _external=True),
                    "cancel_url": url_for('cart', _external=True)
                },
                "transactions": [{
                    "amount": {
                        "total": f"{total:.2f}",
                        "currency": "USD"
                    },
                    "description": f"Pago de carrito ID: {id_venta}"
                }]
            })

            if payment.create():
                for link in payment.links:
                    if link.rel == "approval_url":
                        return redirect(link.href)  # Redirige a PayPal
            else:
                flash("Error al crear el pago en PayPal", "danger")

    except mysql.connector.Error as e:
        conexion.rollback()
        flash(f'Error al procesar el pago: {str(e)}', 'danger')

    finally:
        cursor.close()
        conexion.close()

    return redirect(url_for('cart'))

@app.route('/execute_payment', methods=['GET'])
def execute_payment():
    payment_id = request.args.get('paymentId')
    payer_id = request.args.get('PayerID')
    id_venta = request.args.get('id_venta')

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        flash("Pago realizado con éxito", "success")
        
        correo_usuario = session.get('mail')
        total = float(payment.transactions[0]['amount']['total'])  # Convertir a número
        correoConfirmacion(correo_usuario, id_venta, total)

        return redirect(url_for('confirmation', id_venta=id_venta))
    else:
        flash("Error al procesar el pago en PayPal", "danger")
        return redirect(url_for('cart'))    



@app.route('/test_email')
def test_email():
    # Imprimir las credenciales de Flask-Mail (¡Cuidado con exponer la contraseña!)
    print("Credenciales de Flask-Mail:")
    print(f"MAIL_SERVER: {app.config.get('MAIL_SERVER')}")
    print(f"MAIL_PORT: {app.config.get('MAIL_PORT')}")
    print(f"MAIL_USE_TLS: {app.config.get('MAIL_USE_TLS')}")
    print(f"MAIL_USERNAME: {app.config.get('MAIL_USERNAME')}")
    print(f"MAIL_PASSWORD: {'*' * len(app.config.get('MAIL_PASSWORD', ''))}")  # Oculta la contraseña
    print(f"MAIL_DEFAULT_SENDER: {app.config.get('MAIL_DEFAULT_SENDER')}")

    # Imprimir el contenido de la sesión
    print("Contenido de la sesión:", session)

    # Enviar un correo de prueba
    print('Enviando correo de prueba...')
    try:
        correoConfirmacion('dmnstrdrslibrary@gmail.com', id_venta=12345, total=100.00)
        return "Correo de prueba enviado. Revisa la consola para ver las credenciales."
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
        return f"Error al enviar el correo: {e}"


if __name__ == '__main__':
    app.run(debug=True)