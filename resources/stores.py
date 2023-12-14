from flask_smorest import Blueprint
from flask.views import MethodView
from flask import request, abort
from uuid import uuid4
from db import DataBase as db, jsonify
from schemas import StoreCreateSchema, StoreUpdateSchema, StoreDeleteSchema

stores_blp = Blueprint("stores",__name__)

@stores_blp.route("/store")
class store(MethodView):
    @stores_blp.response(200,StoreUpdateSchema(many=True))
    def get(self):
        query_header = ["store_id", "name"]
        query_output = db.execute_query("SELECT * FROM STORES")
        json_result = jsonify(query_header,query_output, key="store_id")
        print(json_result)
        return json_result.values()

    @stores_blp.arguments(StoreCreateSchema)
    @stores_blp.response(200,StoreUpdateSchema)
    def post(self,store_json):
        query_header = ["store_id", "name"]
        query_output = db.execute_query(f"""INSERT INTO STORES (store_name) VALUES ("{store_json["name"]}") RETURNING store_id, store_name""")
        json_result = jsonify(query_header,query_output)
        return json_result[0]

    @stores_blp.arguments(StoreUpdateSchema)
    @stores_blp.response(200,StoreUpdateSchema)
    def put(self,updated_store_json):
        query_output = db.execute_query(f"""UPDATE STORES SET STORE_NAME = "{updated_store_json["name"]}" WHERE STORE_ID = {updated_store_json["store_id"]} RETURNING STORE_ID, STORE_NAME""")
        if len(query_output) == 0:
            abort(404,"Store not found")
        query_header = ["store_id", "name"]
        json_result = jsonify(query_header,query_output)
        return json_result[0]
        

    @stores_blp.arguments(StoreDeleteSchema)
    @stores_blp.response(200,StoreUpdateSchema)
    def delete(self,delete_store_json):
        query_output = db.execute_query(f"""DELETE FROM STORES WHERE STORE_ID = {delete_store_json["store_id"]} RETURNING STORE_ID, STORE_NAME""")
        if len(query_output) == 0:
            abort(404,"Store not found")
        query_header = ["store_id", "name"]
        json_result = jsonify(query_header,query_output)
        return json_result[0]