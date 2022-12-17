
from flask import Blueprint
from flask.wrappers import Response
from src.app import mongo_client
from bson import json_util
from pymongo import ASCENDING, DESCENDING
from src.app.middlewares.auth import has_logged

inventors = Blueprint("inventors", __name__,  url_prefix="/inventory")

@inventors.route("/analytics", methods = ["GET"])
@has_logged()
def get_analytics():
    result = dict()
    collabs = mongo_client.collabs.count_documents({})
    response_collabs=json_util.dumps(collabs)
    result['Num_Colabs'] = int(response_collabs)
    items = mongo_client.items.count_documents({})
    response_itens=json_util.dumps(items)
    result['Num_Items'] = int(response_itens)
    ItemsPrice = mongo_client.items.aggregate([
     {
        '$group': {
            '_id': '$groupField', 
            'val': {
                '$sum': '$valor'
            }
        }
    }, {
        '$project': {
            '_id': 0
        }
    }
    ])
    respo3=json_util.dumps(ItemsPrice)
    indexInicial = respo3.index(':')+2
    indexFinal = len(respo3)-2
    result['Valor_Items'] = round(float(respo3[indexInicial:indexFinal]),2)
    borrow = mongo_client.items.count_documents({'emprestado' :{'$ne': 'Item disponível'}})
    responseBorrow=json_util.dumps(borrow)
    result['Num_Emprestimos'] = int(responseBorrow)
    resultFinal = json_util.dumps(result)
    return Response(resultFinal ,status=200,mimetype="application/json")

    
    
 



    
