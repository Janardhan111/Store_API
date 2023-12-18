from flask_smorest import Blueprint
from flask.views import MethodView
from schemas import ItemCreateSchema, PlaneItemSchema, ItemSchema
from flask import abort
from uuid import uuid4
from db import DataBase as db, jsonify

items_blp = Blueprint("items",__name__)

@items_blp.route("/items")
class item(MethodView):
    @items_blp.response(200,PlaneItemSchema(many=True))
    def get(self):
        query_output = db.execute_query(f"""SELECT * FROM ITEMS""")
        query_header = ["item_id", "item_name", "item_price" , "store_id"]
        json_result = jsonify(query_header,query_output,key="item_id")
        return json_result.values()

    @items_blp.arguments(ItemCreateSchema)
    @items_blp.response(200,PlaneItemSchema)
    def post(self,item_json):
        query_output = db.execute_query(f"""SELECT * FROM STORES WHERE STORE_ID = "{item_json["store_id"]}";""")
        if len(query_output) == 0:
            abort(404,"Store not found")
        query_header = ["item_id", "item_name", "item_price" , "store_id"]
        query_output = db.execute_query(f"""INSERT INTO ITEMS (item_name,item_price,store_id) VALUES ("{item_json["item_name"]}","{item_json["item_price"]}","{item_json["store_id"]}") RETURNING ITEM_ID, ITEM_NAME, ITEM_PRICE, STORE_ID""")
        json_result = jsonify(query_header,query_output)
        return json_result[0]

    
        
@items_blp.route("/items/<item_id>")
class items_class_with_id(MethodView):
    
    @items_blp.response(200,ItemSchema)
    def get(self,item_id):
        item_header = ["item_id", "item_name", "item_price" , "store_id"]
        item_details = db.execute_query(f"""SELECT * FROM ITEMS WHERE ITEM_ID = {item_id}""")
        if len(item_details) == 0:
            abort(404,"Item not found")
        json_result = jsonify(item_header,item_details)
        store_header = ["store_id", "store_name"]
        store_details = db.execute_query(f"""SELECT STORES.STORE_ID, STORES.STORE_NAME FROM STORES INNER JOIN ITEMS ON ITEMS.STORE_ID = STORES.STORE_ID WHERE ITEMS.ITEM_ID = {item_id}""")
        json_store_item_details = jsonify(store_header,store_details)
        json_result[0]["store"] = json_store_item_details[0]
        return json_result[0]

    @items_blp.arguments(ItemCreateSchema)
    @items_blp.response(200,PlaneItemSchema)
    def put(self,updated_item_json,item_id):
        query_output = db.execute_query(f"""UPDATE ITEMS SET ITEM_NAME = "{updated_item_json["item_name"]}", ITEM_PRICE = "{updated_item_json["item_price"]}", STORE_ID = "{updated_item_json["store_id"]}" WHERE ITEM_ID = {item_id} RETURNING ITEM_ID, ITEM_NAME, ITEM_PRICE, STORE_ID""")
        if len(query_output) == 0:
            abort(404,"Item not found")
        query_header = ["item_id", "item_name", "item_price" , "store_id"]
        json_result = jsonify(query_header,query_output)
        return json_result[0]

    @items_blp.response(200,PlaneItemSchema)
    def delete(self,item_id):
        query_output = db.execute_query(f"""DELETE FROM ITEMS WHERE ITEM_ID = {item_id} RETURNING ITEM_ID, ITEM_NAME, ITEM_PRICE, STORE_ID""")
        if len(query_output) == 0:
            abort(404,"Item not found")
        query_header = ["item_id", "item_name", "item_price" , "store_id"]
        json_result = jsonify(query_header, query_output)
        return json_result[0]