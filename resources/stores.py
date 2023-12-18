from flask_smorest import Blueprint
from flask.views import MethodView
from flask import request, abort
from uuid import uuid4
from db import DataBase as db, jsonify
from schemas import StoreCreateSchema, PlaneStoreSchema, StoreSchema

stores_blp = Blueprint("stores",__name__)

@stores_blp.route("/stores")
class stores_class(MethodView):
    @stores_blp.response(200,PlaneStoreSchema(many=True))
    def get(self):
        query_header = ["store_id", "store_name"]
        query_output = db.execute_query("SELECT * FROM STORES")
        json_result = jsonify(query_header,query_output, key="store_id")
        return json_result.values()

    @stores_blp.arguments(StoreCreateSchema)
    @stores_blp.response(200,PlaneStoreSchema)
    def post(self,store_json):
        query_header = ["store_id", "store_name"]
        query_output = db.execute_query(f"""INSERT INTO STORES (store_name) VALUES ("{store_json["store_name"]}") RETURNING store_id, store_name""")
        json_result = jsonify(query_header,query_output)
        return json_result[0]

@stores_blp.route("/stores/<store_id>")
class store_class_with_id(MethodView):
    @stores_blp.response(200,StoreSchema)
    def get(self,store_id):
        store_header = ["store_id", "store_name"]
        store_details = db.execute_query(f"""SELECT * FROM STORES WHERE STORE_ID = {store_id}""")
        if len(store_details) == 0:
            abort(404, "Store not found")
        json_result = jsonify(store_header,store_details)
        store_items_header = ["item_id", "item_name", "item_price" , "store_id"]
        store_items_details = db.execute_query(f"""SELECT * FROM ITEMS WHERE STORE_ID={store_id}""")
        json_store_item_details = jsonify(store_items_header,store_items_details)
        json_result[0]["items"] = json_store_item_details
        return json_result[0]
    
    @stores_blp.arguments(StoreCreateSchema)
    @stores_blp.response(200,PlaneStoreSchema)
    def put(self,updated_store_json,store_id):
        query_output = db.execute_query(f"""UPDATE STORES SET STORE_NAME = "{updated_store_json["store_name"]}" WHERE STORE_ID = {store_id} RETURNING STORE_ID, STORE_NAME""")
        if len(query_output) == 0:
            abort(404,"Store not found")
        query_header = ["store_id", "store_name"]
        json_result = jsonify(query_header,query_output)
        return json_result[0]

    @stores_blp.response(200,PlaneStoreSchema)
    def delete(self,store_id):
        query_output = db.execute_query(f"""DELETE FROM STORES WHERE STORE_ID = {store_id} RETURNING STORE_ID, STORE_NAME""")
        if len(query_output) == 0:
            abort(404,"Store not found")
        query_header = ["store_id", "store_name"]
        json_result = jsonify(query_header,query_output)
        return json_result[0]