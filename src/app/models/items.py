def create_collection_items(mongo_client):
    items_validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["_id","patrimonio", "titulo", "categoria", "valor", "marca", "modelo", "descricao"],
            "properties": {
                "_id": {
                  "bsonType": "objectId",
                  "description": "Chave definida da collection"
                },
                "patrimonio": {
                  "bsonType": "string",
                  "description": "Número do patrimônio",
                },
                "titulo": {
                  "bsonType": "string",
                  "description": "Título do item",
                },
                "categoria": {
                  "bsonType": "string",
                  "description": "Categoria do item"
                },
                "valor": {
                  "bsonType": "double",
                  "description": "Valor em reais",
                },
                "url": {
                  "bsonType": "string",
                  "description": "url da imagem"
                },
                "marca": {
                  "bsonType": "string",
                  "description": "Marca do item"
                },
                "modelo": {
                  "bsonType": "string",
                  "description": "Modelo do item"
                },
                "descricao": {
                  "bsonType": "string",
                  "description": "Descrição do item"
                },
                "emprestado": {
                  "bsonType": "string",
                  "description": "Status de emprestado"
                },
            },
        }
    }

    try:
        mongo_client.create_collection("items")
    except Exception as e:
        print(e)

    mongo_client.command("collMod", "items", validator=items_validator)