from connection_db import get_db_connection, secret_key
from flask import Flask, jsonify, render_template, request, flash, redirect, url_for, session
import mysql.connector 
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = secret_key()

#redirige a la pagina que muestra los usuarios
@app.route('/usuarios')
def showUsers():
    return render_template('showUsers.html')

@app.route('/indexPage')
def indexPage():
    if 'mail' not in session:
        flash("Debes iniciar sesión para acceder a esta página.", "error")
        return redirect(url_for('loginPage'))

    return render_template('indexPage.html', nombre=session['nombre'])

@app.route('/logout')
def logout():
    session.clear()
    flash("Sesión cerrada exitosamente.", "success")
    return redirect(url_for('loginPage'))

#redirige al index de la pagina despues de validar las credenciales
@app.route('/', methods=['GET', 'POST'])
def loginPage():
    if request.method == 'POST':
        mail = request.form.get('mail')
        passwd = request.form.get('contrasena')

        if not mail or not passwd:
            flash("Todos los datos deben ser ingresados", "error")
            return render_template('login.html')

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.callproc('validateUser', [mail])

            user = None
            for result in cursor.stored_results():
                user = result.fetchone()

            if user and check_password_hash(user['contrasena'], passwd):
                flash("Inicio de sesión exitoso", "success")
                
                session['mail'] = user['mail']
                session['nombre'] = user['nombre']
                session['rol'] = user['rol']
                session['direccion'] = user['direccion']
                session['telefono'] = user['telefono']
                session['contrasena'] = user['contrasena']
                
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
    direccion = request.form['direccion']
    contrasena = request.form['contrasena']
    
    if not nombre or not rol or not telefono or not mail or not direccion or not contrasena:
        flash("Todos los campos son obligatorios.", "error")
        return redirect(url_for('readUsers'))
    
    hashed_password = generate_password_hash(contrasena)
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.callproc('insertUser', [nombre, rol, telefono, mail, direccion, hashed_password]) 
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
    direccion = request.form['direccion']
    contrasena = request.form['contrasena']
        
    if not nombre or not rol or not telefono or not mail or not direccion:
        flash("Todos los campos son obligatorios.", "error")
        return redirect(url_for('readUsers'))
    
    hashed_password = generate_password_hash(contrasena)
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.callproc('updateUser', [user_id, nombre, rol, telefono, mail, direccion, hashed_password])
 
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
    año_publicacion = request.form['año_publicacion']
    stock = request.form['stock']
    genero = request.form['genero']
    estado = request.form['estado']
    
    if not nombre or not autor or not año_publicacion or not stock or not genero or not estado:
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
        cursor.callproc('insertBook', [nombre, autor, año_publicacion, stock, genero, estado])
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
                libro['fecha_pub'] = datetime.strptime(str(libro['fecha_pub']), '%Y-%m-%d %H:%M:%S')
                libro['es_nuevo'] = (ahora - libro['fecha_pub']) < timedelta(hours=24)
        
        
    except mysql.connector.Error as error:
        print(f"Error MySQL: {error}")  
        flash(f"Error al obtener los libros: {error}", "error")
        libros = []

    finally:
        cursor.close()
        conn.close()
    print(libros)
    return render_template('/showBooks.html', libros = libros)

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
    año_publicacion = request.form.get('año_publicacion')
    stock = request.form.get('stock')
    genero = request.form.get('genero')
    fecha_pub = request.form.get('fecha_pub')
    estado = request.form.get('estado')
    id_libro = request.form.get('id')

    if not all([nombre, autor, año_publicacion, stock, genero, fecha_pub, estado, id_libro]):
        flash("Todos los campos son obligatorios.", "error")
        return redirect(url_for('readBooks'))

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.callproc('updateLibro', [id_libro, nombre, autor, año_publicacion, stock, genero, fecha_pub, estado])
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
    if 'mail' not in session:
        flash("Debe iniciar sesión primero", "error")
        return redirect(url_for('loginPage'))
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        direccion = request.form.get('direccion')
        telefono = request.form.get('telefono')
        contrasena_actual = request.form.get('contrasena_actual')
        nueva_contrasena = request.form.get('nueva_contrasena')
        confirmar_contrasena = request.form.get('confirmar_contrasena')
        
        conn = None
        cursor = None
        
        try:
            if not nombre or not direccion or not telefono:
                flash("Nombre, dirección y teléfono son obligatorios", "error")
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
                    direccion, 
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
                    direccion, 
                    telefono
                ])
            
            conn.commit()
            
            session['nombre'] = nombre
            session['direccion'] = direccion
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
                          direccion=session.get('direccion', ''),
                          telefono=session.get('telefono', ''),
                          mail=session.get('mail', ''))

if __name__ == '__main__':
    app.run(debug=True)