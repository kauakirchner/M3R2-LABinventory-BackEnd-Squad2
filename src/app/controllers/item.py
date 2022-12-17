
from flask import Blueprint, request, jsonify
from flask.wrappers import Response
from src.app import mongo_client
from bson import json_util, ObjectId
from src.app.middlewares.auth import required_fields, has_logged
from src.app.middlewares.items import item_exists


items = Blueprint("items", __name__,  url_prefix="/items")

@items.route("/", methods = ["GET"])
@has_logged()
def get_all_items():
    title = request.args.get('title')
    if title:
        list_items_per_title = mongo_client.items.find({"titulo": { "$regex": title}})
        if not list_items_per_title:
            error = {
                "Error": "Item não encontrado."
            }
            return jsonify(error), 204

        return Response(
            response=json_util.dumps({"records": list_items_per_title}),
            status=200,
            mimetype="application/json")

    items = mongo_client.items.find()
    return Response(
    response=json_util.dumps({'records' : items}),
    status=200,
    mimetype="application/json"
  )

@items.route("/", methods=["POST"])
@has_logged()
@required_fields(["patrimonio", "titulo", "categoria", "valor", "marca", "modelo", "descricao", "url"])
@item_exists()
def insert_item():
    item = request.get_json()

    if(float(item["valor"])<=0.0):
        return {"error": "Valor tem que ser maior que zero"}, 400

    elif(float(item["valor"])>0):
        mongo_client.items.insert_one(item)

        return {"sucesso": "Item cadstrado com sucesso"}, 201
    else:
        return {"error": "Erro ao cadastrar item"}, 400
    
    
@items.route("/<patr>", methods=["DELETE"])
@has_logged()
def delete_item(patr):
    try:
        mongo_client.items.delete_one({'patrimonio': patr})
        return {"sucesso": "Item deletado com sucesso"}, 200
    except Exception:
        return {"error": "Algo deu errado."}, 500

@items.route("/", methods=["PATCH"])
@has_logged()
@required_fields(["patrimonio", "titulo", "categoria", "valor", "marca", "modelo", "descricao", "url"])
def edit_item():
    id_item = request.args.get("_id")
    new_item = request.get_json()

    update_item = mongo_client.items.update_one({"_id": ObjectId(id_item)},
        {
            "$set": {
                        "patrimonio": new_item['patrimonio'],
                        "titulo": new_item['titulo'],
                        "categoria": new_item['categoria'],
                        "valor": new_item['valor'],
                        "url": new_item['url'],
                        "marca": new_item['marca'],
                        "modelo": new_item['modelo'],
                        "descricao": new_item['descricao'],
                        "emprestado": new_item['emprestado']
                    }
        })
    if update_item:
        return {"sucesso": f"Item {new_item['titulo']} atualizado com sucesso"}, 200
    return {"error": "Erro ao tentar atualizar item"}, 401