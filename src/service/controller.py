from flask import request, Response, redirect, url_for
from bson import json_util, ObjectId
from datetime import datetime  # Importar datetime

from config.mongodb import mongo


def create_lista_service():
    producto = request.form.get("producto")
    precio = request.form.get("precio")
    if producto:
        current_time = datetime.now()
        response = mongo.db.lista.insert_one(
            {
                "producto": producto,
                "precio": precio,
                "done": False,
                "last_modified": current_time,
            }
        )
        return redirect(url_for("Home"))
    else:
        return "Invalid payload", 400


def get_listas_service():
    data = mongo.db.lista.find().sort(
        "last_modified", -1
    )  # Ordenar por last_modified en orden descendente
    result = json_util.dumps(data)
    return Response(result, mimetype="application/json")


def get_lista_service(id):
    data = mongo.db.lista.find_one({"_id": ObjectId(id)})
    result = json_util.dumps(data)
    return Response(result, mimetype="application/json")


def delete_lista_service(id):
    if request.method == "POST" and request.form.get("_method") == "DELETE":

        response = mongo.db.lista.delete_one({"_id": ObjectId(id)})
        if response.deleted_count >= 1:
            return redirect(url_for("Home"))
    return "Lista not found", 404


def update_lista_service(id):
    if request.method == "POST":
        producto = request.form.get("producto")
        precio = request.form.get("precio")
        data = {
            "producto": producto,
            "precio": precio,
            "last_modified": datetime.now(),  # Actualizar la fecha de modificación
        }
        if producto:
            response = mongo.db.lista.update_one({"_id": ObjectId(id)}, {"$set": data})
            if response.modified_count >= 1:
                return redirect(url_for("Home"))
    return "Invalid payload or Lista not found", 400
