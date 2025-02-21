import mysql.connector 
from flask import Flask, jsonify, render_template, request, flash, redirect, url_for

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
    key = 'Nachitwo'
    return key
