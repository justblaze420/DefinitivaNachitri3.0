import mysql.connector 
from flask import Flask, jsonify, render_template, request, flash, redirect, url_for
import secrets
from flask_mail import Mail, Message

print(secrets.token_hex(16))

app = Flask(__name__)

# Configuración de la conexión
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'EmpireLibrary'
}

# Función para obtener la conexión a la base de datos
def get_db_connection():
    return mysql.connector.connect(**db_config)

def secret_key():
    key = '3e8c6612af86d9b5ad6a4f1f4d428256'
    return key

mail = Mail()

def init_mail(app): 
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'dmnstrdrslibrary@gmail.com'
    app.config['MAIL_PASSWORD'] = 'xity qnrb ibny vzqk'
    app.config['MAIL_DEFAULT_SENDER'] = 'dmnstrdrslibrary@gmail.com'
    
    mail.init_app(app)

init_mail(app)

def correoConfirmacion(destinatario, id_venta, total):
    asunto = 'Confirmación de Compra'
    cuerpo = f'''
    Gracias por tu compra.
    
    Detalles de la compra:
    - ID de Venta: {id_venta}
    - Total: ${total:.2f}
    
    ¡Esperamos que disfrutes tu compra!
    '''

    # Crear el mensaje
    mensaje = Message(
        subject=asunto,
        recipients=[destinatario],  # Lista de destinatarios
        cc=['dmnstrdrslibrary@gmail.com'],  # Lista de destinatarios en copia
        body=cuerpo
    )

    # Enviar el correo
    try:
        mail.send(mensaje)
        print('Correo enviado con éxito')
    except Exception as e:
        print(f'Error al enviar el correo: {e}')