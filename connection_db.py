import mysql.connector 
from flask import Flask, jsonify, render_template, request, flash, redirect, url_for
import secrets

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
