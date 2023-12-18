from flask import request, Response, redirect, url_for,send_file
from bson import json_util, ObjectId
from datetime import datetime  # Importar datetime
from openpyxl import Workbook
from io import BytesIO
from config.mongodb import mongo
import json

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
def excel_generate():
  
    file_path = create_excel()
    return send_file(
        file_path,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name='datos.xlsx'  # Nombre del archivo para descargar
    )

def create_excel():   
    data = mongo.db.lista.find().sort(
        "last_modified", -1
    )  # Ordenar por last_modified en orden descendente
    data_json = json_util.dumps(data)
    # Cargar los datos JSON
    data = json.loads(data_json)

    wb = Workbook()
    ws = wb.active
    # Escribir encabezados de columna en la hoja de cálculo
    # headers = list(data[0].keys())
    # ws.append(headers)
    filtered_headers = ["producto", "precio"]
    ws.append(filtered_headers)
   # Escribir datos en la hoja de cálculo
    for item in data:
        row_data = [str(item.get(header, '')) for header in filtered_headers]
        ws.append(row_data)

    # Crear un archivo en memoria
    excel_file = BytesIO()
    wb.save(excel_file)
    # wb.save('datos.xlsx')
    excel_file.seek(0)

    return excel_file
