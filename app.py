#Importaciones de flask y funcionalidades
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_mysqldb import MySQL
import config


# Creacion de instacia de Flask
app = Flask(__name__)

# Coneccion al config.py
app.config['SECRET_KEY'] = config.HEX_SEC_KEY
app.config['MYSQL_HOST'] = config.MYSQL_HOST
app.config['MYSQL_USER'] = config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = config.MYSQL_DB

# Instancia de MySQL
mysql = MySQL(app)


# Ruta Principal de la aplicacion 
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

# Ruta de la aplicacion para el login
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    #Coneccion a la base de datos
    cur = mysql.connection.cursor()
    #Consulta a la base de datos para saber si el usuario existe
    cur.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email, password))


if __name__ == '__main__':
    app.run(debug=True)