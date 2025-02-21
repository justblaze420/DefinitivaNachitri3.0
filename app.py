from connection_db import get_db_connection, secret_key
from flask import Flask, jsonify, render_template, request, flash, redirect, url_for
import mysql.connector 

app = Flask(__name__)
app.secret_key = secret_key()

#redirige al index de la pagina
@app.route('/')
def indexPage():
    return render_template('indexPage.html')

#redirige a la pagina que muestra los usuarios
@app.route('/usuarios')
def showUsers():
    return render_template('showUsers.html')

#Creacion de usuarios
@app.route('/createUsers',methods=['GET','POST'])
def createUsers():
    nombre = request.form['nombre']
    rol = request.form['rol']
    telefono = request.form['telefono']
    mail = request.form['mail']
    direccion = request.form['direccion']
    
    if not nombre or not rol or not telefono or not mail or not direccion:
        flash("Todos los campos son obligatorios.", "error")
        return redirect(url_for('readUsers'))
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.callproc('insertUser1', [nombre, rol, telefono, mail, direccion]) 
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

    if not nombre or not rol or not telefono or not mail or not direccion:
        flash("Todos los campos son obligatorios.", "error")
        return redirect(url_for('readUsers'))
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.callproc('updateUser', [user_id, nombre, rol, telefono, mail, direccion])
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