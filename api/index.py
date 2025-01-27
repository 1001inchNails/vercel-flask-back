from flask import Flask,jsonify,request
from flask_pymongo import PyMongo
from pymongo import MongoClient
from flask_cors import CORS 

app = Flask(__name__)
CORS(app)

client = MongoClient('mongodb+srv://dccAtlMongoC_S:1001%25%25wWqq4904@clusterbuster.bl5p1.mongodb.net/?retryWrites=true&w=majority&appName=ClusterBuster')
db = client['exendpovercel']
collection = db['usuarios']


def listadoUsers():
    cursor = collection.find()
    listaUsuarios = []
    for doc in cursor:
        doc['_id']=str(doc['_id'])
        listaUsuarios.append(doc)
    return listaUsuarios


def insertarNuevoDocumento(nuevoDoc):
  try:
    collection.insert_one(nuevoDoc)
  except:
    print("ERROR: Fallo al introducir nuevo usuario")
  else:
    print("Nuevo usuario registrado correctamente")
    


@app.route('/')
def home():
    return 'Sup, bitches!'

@app.route('/api/users',methods=["GET"])
def users():
    usuarios=listadoUsers()
    print(type(usuarios))
    return usuarios

#ejemplo (body): {"nombre":"Zeus2","apellidos":"Perez Colina","email":"zeusPC@mainModule.com","telefono":"610445846"}
@app.route('/api/users',methods=["POST"])
def new_users():
    listaUsuarios=listadoUsers()
    id=len(listaUsuarios)
    id+=1
    id=str(id)
    nuevo_user=request.get_json()
    nuevo_user.update({"id":id})
    print(nuevo_user)
    print(type(nuevo_user))
    insertarNuevoDocumento(nuevo_user)
    return 'ay caramba'

# ruta/api/usersByName?nombre=loquesea
@app.route('/api/usersByName',methods=["GET"])
def get_user_by_name():
    resultado = []
    user_nombre = request.args.get('nombre')
    
    cursor = collection.find({'nombre': user_nombre})
    
    for document in cursor:
        document['_id']=str(document['_id'])
        resultado.append(document)
    if resultado:
        return jsonify({"mensaje": "Usuario introducido correctamente"})
    elif not resultado:
        return "No se han encontrado coincidencias"


app.run()