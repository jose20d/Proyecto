from flask import Flask, render_template, request, jsonify
from flask_api import status
import configparser
import psycopg2

app = Flask(__name__)
config = configparser.ConfigParser()
config.read('padronapi.ini')
cnx=psycopg2.connect(dbname=config['DB']['name'], user=config['DB']['user'], password=config['DB']['password'], host=config['DB']['host'], port=config['DB']['port'])
cur=cnx.cursor()

@app.route('/')
def index():
    return render_template('home.html')

#Generales
	#Provicias
@app.route('/api/v1/provincias',methods=['POST', 'GET', 'DELETE', 'PUT'])
def provincias():
    if request.method == 'GET':
        cur.execute("SELECT nombre FROM provincia;")
        dataJson = []
        for provincia in cur.fetchall():
            dataDict = {                
                'nombre': provincia[0]
            }
            dataJson.append(dataDict)
        return jsonify(dataJson), status.HTTP_200_OK
    else :
        content = {'Error de metodo': 'Solo se soporta GET para provincias'}
        return content, status.HTTP_405_METHOD_NOT_ALLOWED

	#Cantones
@app.route('/api/v1/cantones',methods=['POST', 'GET', 'DELETE', 'PUT'])
def cantones():
    if request.method == 'GET':
        cur.execute("SELECT provincia, codigo, nombre FROM canton;")
        dataJson = []
        for cantones in cur.fetchall():
            dataDict = {
		'provincia':cantones[0],
                'codigo': cantones[1],
                'nombre': cantones[2]
            }
            dataJson.append(dataDict)
        return jsonify(dataJson), status.HTTP_200_OK
    else :
        content = {'Error de metodo': 'Solo se soporta GET para cantones'}
        return content, status.HTTP_405_METHOD_NOT_ALLOWED

	#Distritos
@app.route('/api/v1/distritos',methods=['POST', 'GET', 'DELETE', 'PUT'])
def distritos():
    if request.method == 'GET':
        cur.execute("SELECT provincia, canton, codigo, nombre FROM distrito;")
        dataJson = []
        for distritos in cur.fetchall():
            dataDict = {
		'provincia':distritos[0],
		'canton':distritos[1],
                'codigo': distritos[2],
                'nombre': distritos[3]
            }
            dataJson.append(dataDict)
        return jsonify(dataJson), status.HTTP_200_OK
    else :
        content = {'Error de metodo': 'Solo se soporta GET para distritos'}
        return content, status.HTTP_405_METHOD_NOT_ALLOWED

#Especificas
	#Provincia
@app.route('/api/v1/provincia/<string:nombre>',methods=['POST', 'GET', 'DELETE', 'PUT'])
def provincia(nombre):
    if request.method == 'GET':
        cur.execute("SELECT codigo FROM provincia WHERE nombre=%s;",(nombre,))
        provincia=cur.fetchone()
        if provincia is None :
            content = {'Error de codigo': 'La provincia con el nombre {} no existe.'.format(nombre)}
            return content, status.HTTP_404_NOT_FOUND
        else :
            dataDict = {
                'codigo': provincia[0]
            }
            return jsonify(dataDict), status.HTTP_200_OK
    else :
        content = {'Error de metodo': 'Solo se soporta GET para provincia'}
        return content, status.HTTP_405_METHOD_NOT_ALLOWED

	#Canton
@app.route('/api/v1/canton/<string:provincia>&<string:nombre>',methods=['POST', 'GET', 'DELETE', 'PUT'])
def canton(nombre, provincia):
    if request.method == 'GET':
        cur.execute("SELECT codigo FROM canton WHERE provincia=%s AND nombre = %s;",(provincia, nombre))
        canton=cur.fetchone()
        if canton is None :
            content = {'Error de codigo': 'El canton con el nombre {} no existe.'.format(nombre)}
            return content, status.HTTP_404_NOT_FOUND
        else :
            dataDict = {
                'codigo': canton[0]
            }
            return jsonify(dataDict), status.HTTP_200_OK
    else :
        content = {'Error de metodo': 'Solo se soporta GET para canton'}
        return content, status.HTTP_405_METHOD_NOT_ALLOWED

	#Distrito
@app.route('/api/v1/distrito/<string:provincia>&<string:canton>&<string:nombre>',methods=['POST', 'GET', 'DELETE', 'PUT'])
def distrito(nombre, provincia, canton):
    if request.method == 'GET':
        cur.execute("SELECT codigo FROM distrito WHERE provincia=%s AND canton=%s AND nombre=%s;",(provincia, canton, nombre))
        distrito=cur.fetchone()
        if distrito is None :
            content = {'Error de codigo': 'El distrito con el codigo {} no existe.'.format(nombre)}
            return content, status.HTTP_404_NOT_FOUND
        else :
            dataDict = {
                'codigo': distrito[0]
            }
            return jsonify(dataDict), status.HTTP_200_OK
    else :
        content = {'Error de metodo': 'Solo se soporta GET para canton'}
        return content, status.HTTP_405_METHOD_NOT_ALLOWED

	#Codigo postal
@app.route('/api/v1/codpostal/<string:codpostal>',methods=['POST', 'GET', 'DELETE', 'PUT'])
def codpostal(codpostal):
    if request.method == 'GET':
        prv = str(codpostal[0:1])
        cant = str(codpostal[1:3])
        dist = str(codpostal[3:7])
	
        cur.execute("SELECT nombre FROM provincia WHERE codigo=%s;",(prv))
        prvnom=cur.fetchone()

        cur.execute("SELECT nombre FROM canton WHERE provincia = %s and codigo=%s;",(prv,cant))
        cantnom=cur.fetchone()

        cur.execute("SELECT nombre FROM distrito WHERE provincia = %s and canton = %s and codigo=%s;",(prv,cant,dist))
        distnom=cur.fetchone()

        if prvnom is None or cantnom is None or distnom is None:
            content = {'Error de codigo': 'El codigo postal {} no existe.'.format(codpostal)}
            return content, status.HTTP_404_NOT_FOUND
        else :
            dataDict = {
                'provincia': prvnom[0],
                'canton': cantnom[0],
                'distrito': distnom[0]
            }
            return jsonify(dataDict), status.HTTP_200_OK
    else :
        content = {'Error de método': 'Solo se soporta POST y GET para canton'}
        return content, status.HTTP_405_METHOD_NOT_ALLOWED

	#Ciudadano 
		#Se coloca como POST solo para probar
@app.route('/api/v1/ciudadano',methods=['POST', 'GET', 'DELETE', 'PUT'])
def ciudadano():
    if request.method == 'POST':
        ced_json = request.get_json()
        ced = ced_json['cedula']
        cur.execute("SELECT vencimiento, sexo, nombre, apellido1, apellido2, provincia, canton, distrito, junta FROM ciudadano WHERE cedula=%s;",(ced,))
        ciudadano=cur.fetchone()
        if ciudadano is None :
            content = {'Error de cedula': 'La cedula {} no existe.'.format(ciudadano)}
            return content, status.HTTP_404_NOT_FOUND
        else :
            dataDict = {
                'vencimiento': ciudadano[0],
                'sexo': ciudadano[1],
                'nombre': ciudadano[2],
                'apellido1': ciudadano[3],
                'apellido2': ciudadano[4],
                'codpostal': ciudadano[5]+ciudadano[6]+ciudadano[7],
                'junta': str(ciudadano[8]),
            }
            return jsonify(dataDict), status.HTTP_200_OK
    else :
        content = {'Error de metodo': 'Solo se soporta GET para canton'}
        return content, status.HTTP_405_METHOD_NOT_ALLOWED
if __name__ == '__main__':
    app.debug = True
    app.run()
