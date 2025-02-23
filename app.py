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

#Funcion para actualizar los users
@app.route('/updateUsers', methods=['GET','POST'])
def updateUsers():
    nombre = request.form['nombre']
    rol = request.form['rol']
    telefono = request.form['telefono']
    mail = request.form['mail']
    direccion = request.form['direccion']
    user_id = request.form['id']
    contrasena = request.form['contrasena']

    if not nombre or not rol or not telefono or not mail or not direccion or not contrasena:
        flash("Todos los campos son obligatorios.", "error")
        return redirect(url_for('readUsers'))
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.callproc('updateUser', [user_id, nombre, rol, telefono, mail, direccion, contrasena])
        conn.commit()
          
        flash("Usuario actualizado correctamente.", "success")
    
    except mysql.connector.Error as error:
        flash(f"Error al actualizado el usuario: {error}", "error")
    
    finally:
        cursor.close()  
        conn.close()
    
    return render_template('showUsers.html')

#Funcion para eliminar a los usuarios
@app.route('/deleteUsers/<int:id>', methods=['POST'])
def deleteUsers(id):
    nombre = request.form['nombre']
    
    if not nombre:
        flash("El nombre es obligatorio para confirmar la eliminación.", "error")
        return redirect(url_for('readUsers'))
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.callproc('deleteUser', [nombre, id]) 
        conn.commit()
        flash("Usuario eliminado correctamente.", "success")
    
    except mysql.connector.Error as error:
        flash(f"Error: {error}", "error")
    
    finally:
        cursor.close()  
        conn.close()
    
    return redirect(url_for('readUsers'))   

if __name__ == '__main__':
    app.run(debug=True)