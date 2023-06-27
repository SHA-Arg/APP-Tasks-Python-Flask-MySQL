#Importaciones de flask y funcionalidades
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_mysqldb import MySQL
import config
from datetime import datetime


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
#definir la funcion
def login():
    email = request.form['email']
    password = request.form['password']

    #Coneccion a la base de datos
    cur = mysql.connection.cursor()
    #Consulta a la base de datos para saber si el usuario existe
    cur.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email, password))
    #Recibir informacion
    user = cur.fetchone()
    #Cerrar coneccion
    cur.close()

    #Si el usuario existe redirigir a la pagina de inicio un mensaje
    if user is not None:
        #variables de sesion
        session['email'] = user
        session['name'] = user[1]
        session['surname'] = user[2]
        return redirect(url_for('tasks'))
    else:
        return render_template('index.html', message='Las credenciales no coinciden')

    # definir la ruta y la funcion del Task
@app.route('/tasks', methods=['GET'])
def tasks():
    email = session['email']
    #Coneccion a la base de datos
    cur = mysql.connection.cursor()
    #Consulta a la base de datos para obtener las tareas del usuario
    cur.execute('SELECT * FROM tasks WHERE email = %s', [email])
    #Recibir informacion
    tasks = cur.fetchall()
    insertObject = []
    columnNames = [column[0] for column in cur.description]
    #Recorrer la informacion
    for record in tasks:
        insertObject.append(dict(zip(columnNames, record)))
    #Cerrar coneccion
    cur.close()

    return render_template('tasks.html', tasks=insertObject)

    #Definir la ruta del logout
@app.route('/logout')
def logout():
    #eliminar las variables de sesion
    session.clear()
    return redirect(url_for('home'))

    #Definir la ruta para nueva tarea
@app.route('/new-task', methods=['POST'])
def newTask():
    title = request.form['title']
    description = request.form['description']
    #obtener el email de la variable de sesion
    email = session['email']
    #obtener fecha del momento de la creacion de la tarea
    d = datetime.now()
    #formatear la fecha
    dateTask = d.strftime("%Y-%m-%d %H:%M:%S")

    #condicion para saber si existen los datos para crear la tarea
    if title and description and email:
        #coneccion a la base de datos
        cur = mysql.connection.cursor()
        #consulta para insertar la tarea
        sql = "INSERT INTO tasks (email, title, description, date_task) VALUES (%s, %s, %s, %s)"
        #recolecion de datos 
        data = (email, title, description, dateTask)
        #ejecutar la consulta
        cur.execute(sql, data)
        #guardar cambios
        mysql.connection.commit()
    #redirigir a la pagina de tareas
    return redirect(url_for('tasks'))

#ruta para nuevo usuario
@app.route('/new-user', methods=['POST'])
#definir la funcion
def newUser():
    #obtener los datos del formulario
    name = request.form['name']
    surname = request.form['surname']
    email = request.form['email']
    password = request.form['password']

    #condicion para saber si existen los datos para crear el usuario
    if name and surname and email and password:
        #coneccion a la base de datos
        cur = mysql.connection.cursor()
        #consulta para insertar el usuario
        sql = 'INSERT INTO users (name, surname, email, password) VALUES (%s, %s, %s, %s)'
        #recolecion de datos
        data = (name, surname, email, password)
        #ejecutar la consulta
        cur.execute(sql, data)
        #guardar cambios
        mysql.connection.commit()
    #redirigir a la pagina de inicio
    return redirect(url_for('tasks'))

    

if __name__ == '__main__':
    app.run(debug=True)