from connection_db import get_db_connection, secret_key
from flask import Flask, jsonify, render_template, request, flash, redirect, url_for, session
import mysql.connector 
from werkzeug.security import generate_password_hash, check_password_hash

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
    
    return render_template('showUsers.html')

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
@app.route('/delete', methods=['POST'])
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
    
    return render_template('showUsers.html')

#libros(nombre, autor, ano_publicacion, stock, genero, fecha_pub, estado)
@app.route('/createBooks', methods=['GET', 'POST'])
def createBooks():
    nombre = request.form['nombre']
    autor = request.form['autor']
    año_publicacion = request.form['año_publicacion']
    stock = request.form['stock']
    genero = request.form['genero']
    fecha_pub = request.form['fecha_pub']
    estado = request.form['estado']
    
    if not nombre or not autor or not año_publicacion or not stock or not genero or not fecha_pub or not estado:
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
        cursor.callproc('insertBook', [nombre, autor, año_publicacion, stock, genero, fecha_pub, estado])
        conn.commit()
        flash("Libro registrado correctamente.", "success")
    
    except mysql.connector.Error as error:
        flash(f"Error al registrar el libro: {error}", "error")
    
    finally:
        cursor.close()  
        conn.close()
    
    return redirect(url_for('showBooks'))

@app.route('/showBooks', methods=['GET'])
def showBooks():    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    libros = [] 
    try:
        cursor.callproc('GetAllBooks')
        print("Procedimiento llamado exitosamente") 
        
        results = cursor.stored_results()
        print("Obteniendo resultados")
        
        for result in results:
            libros = result.fetchall() 

    except mysql.connector.Error as error:
        print(f"Error MySQL: {error}")  
        flash(f"Error al obtener los libros: {error}", "error")
        libros = []

    finally:
        cursor.close()
        conn.close()
    print(libros)
    return render_template('/showBooks.html', libros = libros)

@app.route('/delete', methods=['POST'])
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

if __name__ == '__main__':
    app.run(debug=True)