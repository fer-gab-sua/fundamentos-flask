    """
    link de curso: https://www.youtube.com/watch?v=-1DmVCPB6H8
    Descripcion: Tutorial Flask: Framework de Python para Aplicaciones Web 🌐 (Desde Cero) ✅
    Esado: Terminado

    """


from flask import Flask, render_template, request , redirect , url_for, jsonify
from flask_mysqldb import MySQL
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
print(os.environ.get("MYSQL_ADDON_HOST"))
# Configuración de la conexión a MySQL
app.config['MYSQL_HOST'] = os.environ.get("MYSQL_ADDON_HOST")
app.config['MYSQL_USER'] = os.environ.get("MYSQL_ADDON_USER")
app.config['MYSQL_PASSWORD'] = os.environ.get("MYSQL_ADDON_PASSWORD")
app.config['MYSQL_DB'] = os.environ.get("MYSQL_ADDON_DB")
app.config['MYSQL_PORT'] = int(os.environ.get("MYSQL_ADDON_PORT"))


conexion = MySQL(app)

@app.before_request
def before_request():
    print("antes de la peticion")

@app.after_request
def after_request(response):
    print("despues de la peticion")
    return response



@app.route('/')
def index():
    cursos = ['php', 'python' , 'java', 'JavaScript']
    data = {
        'titulo': 'Index',
        'bienvenida': 'saludos',
        'cursos':cursos,
        "numero_cursos":len(cursos)
    }
    return render_template('index.html', data=data)

@app.route('/contacto/<nombre>/<int:edad>')
def contacto(nombre, edad):
    data={
        'titulo':'Contacto',
        'nombre':nombre,
        'edad':edad
    }
    return render_template('contacto.html', data=data)

def query_string():
    print(request)
    print(request.args)
    print(request.args.get('param1'))
    print(request.args.get('param2'))
    return "ok"

def pagina_no_encontrada(error):
    data = {
    'titulo': 'Página no encontrada'
    }
    #return render_template('404.html',data=data),404
    return redirect(url_for('index'))


@app.route('/cursos')
def listar_cursos():
    data = {}
    try:
        cursor = conexion.connection.cursor()
        sql="SELECT * FROM cursos.cursos"
        cursor.execute(sql)
        cursos = cursor.fetchall()
        data['cursos'] = cursos
        data['mensaje'] = 'exito'
        print(cursos)
    except Exception as ex:
        data['mensaje'] = 'Error...'
        print(ex)
    return jsonify(data)


if __name__ == '__main__':
    app.add_url_rule('/query_string', view_func=query_string) #ejemplo de querystring = http://127.0.0.1:5000/query_string?param1=Jorge&param2=Jose
    app.register_error_handler(404,pagina_no_encontrada)
    app.run(debug=True, port=5000)