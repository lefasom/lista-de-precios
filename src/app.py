import os
from flask import Flask, render_template
from dotenv import load_dotenv
from bson import ObjectId
from config.mongodb import mongo
from routes.rutas import rutas

load_dotenv()

app = Flask(__name__)

app.config["MONGO_URI"] = os.getenv("MONGO_URI")

mongo.init_app(app)


@app.route("/") #decorador
def Home():
    cursor = mongo.db.lista.find().sort("last_modified", -1)  # Ordenar por last_modified en orden descendente
    listas = list(cursor)  # Convierte el cursor a una lista
    return render_template('index.html', listas=listas)


@app.route("/crear")
def Crear():
    return render_template("crear.html")

@app.route("/editar/<id>")
def Editar(id):
    id = ObjectId(id)
    producto = mongo.db.lista.find_one({"_id": id})
    
    return render_template('editar.html', producto=producto)

app.register_blueprint(rutas, url_prefix="/rutas")
if __name__ == "__main__":
    app.run(debug=True)

