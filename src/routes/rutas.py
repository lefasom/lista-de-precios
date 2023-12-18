from flask import Blueprint, request

from service.controller import (
    create_lista_service,
    get_listas_service,
    get_lista_service,
    update_lista_service,
    delete_lista_service,
    excel_generate,    
)

rutas = Blueprint("rutas", __name__)

# @rutas.route('/', methods=['GET'])
# def get_listas():
#     return get_listas_service()

# @rutas.route('/<id>',methods=['GET'])
# def get_lista(id):
#     return get_lista_service(id)


@rutas.route("/", methods=["POST"])
def create_lista():
    return create_lista_service()


@rutas.route("/<id>", methods=["POST"])
def lista(id):
    if request.form.get("_method") == "DELETE":
        return delete_lista_service(id)
    return update_lista_service(id)


@rutas.route("/", methods=["GET"])
def export_excel():
    return excel_generate()
