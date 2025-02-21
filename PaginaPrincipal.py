from flask import Flask, jsonify, render_template, request, flash, redirect, url_for
from conexionSQL import get_db_connection, mysql, secret_key


app = Flask(__name__)
app.secret_key = secret_key()


#Pagina principal
@app.route('/')
def index_pagina():
    return render_template('index_page.html')


#ir al formulario para crear usuarios
@app.route('/formulario')
def formulario():
    return render_template('formulario.html')

#Eliminar gente
@app.route('/formulario2')
def formulario2():
    return render_template('/formulario2')

#Añadir usuario
@app.route('/create', methods=['POST'])
def create():
    nombre = request.form['nombre']
    rol = request.form['rol']
    telefono = request.form['telefono']
    mail = request.form['mail']
    direccion = request.form['direccion']
    
    if not nombre or not rol or not telefono or not mail or not direccion:
        flash("Todos los campos son obligatorios.", "error")
        return redirect(url_for('formulario'))

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

    return redirect(url_for('formulario'))


#Eliminar usuario
@app.route('/delete', methods=['POST'])
def delete():
    nombre = request.form['nombre']
    id_usuario = request.form['id_usuario']
    
    if not nombre or not id_usuario:
        flash("Todos los campos son obligatorios.", "error")
        return redirect(url_for('formulario'))

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.callproc('deleteUser', [nombre, id_usuario]) 
        conn.commit()
          
        flash("Usuario eliminado correctamente.", "success")
    except mysql.connector.Error as error:
        flash(f"Error al registrar el usuario: {error}", "error")
    finally:
        cursor.close()  
        conn.close()

    return redirect(url_for('formulario2'))



#Metodo que llama a la pagina donde se muestran todos los usuarios
@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.callproc('GetAllUsers')  
    conn.commit()

    # Obtener los resultados
    for result in cursor.stored_results():
        usuarios = result.fetchall()

    conn.close()
    return render_template('usuarios.html', usuarios=usuarios)

if __name__ == '__main__':
    app.run(debug=True)