from flask_smorest import Blueprint
from flask.views import MethodView
from schemas import ItemCreateSchema, ItemUpdateSchema, ItemDeleteSchema
from flask import abort
from uuid import uuid4
from db import DataBase as db, jsonify

items_blp = Blueprint("items",__name__)

@items_blp.route("/items")
class item(MethodView):
    # @items_blp.response(200,ItemUpdateSchema(many=True))
    def get(self):
        query_output = db.execute_query(f"""SELECT * FROM ITEMS""")
        query_header = ["item_id", "item_name", "item_price" , "store_id"]
        json_result = jsonify(query_header,query_output,key="item_id")
        print(json_result)
        return json_result

    @items_blp.arguments(ItemCreateSchema)
    @items_blp.response(200,ItemUpdateSchema)
    def post(self,item_json):
        query_output = db.execute_query(f"""SELECT * FROM STORES WHERE STORE_ID = "{item_json["store_id"]}";""")
        if len(query_output) == 0:
            abort(404,"Store not found")
        query_header = ["item_id", "item_name", "item_price" , "store_id"]
        query_output = db.execute_query(f"""INSERT INTO ITEMS (item_name,item_price,store_id) VALUES ("{item_json["item_name"]}","{item_json["item_price"]}","{item_json["store_id"]}") RETURNING ITEM_ID, ITEM_NAME, ITEM_PRICE, STORE_ID""")
        json_result = jsonify(query_header,query_output)
        return json_result[0]

    @items_blp.arguments(ItemUpdateSchema)
    @items_blp.response(200,ItemUpdateSchema)
    def put(self,updated_item_json):
        query_output = db.execute_query(f"""SELECT * FROM ITEMS WHERE ITEM_ID = {updated_item_json["item_id"]};""")
        if len(query_output) == 0:
            abort(404,"Item not found")
        query_header = ["item_id", "item_name", "item_price" , "store_id"]
        query_output = db.execute_query(f"""UPDATE ITEMS SET ITEM_NAME = "{updated_item_json["item_name"]}", ITEM_PRICE = "{updated_item_json["item_price"]}", STORE_ID = "{updated_item_json["store_id"]}" WHERE ITEM_ID = {updated_item_json["item_id"]} RETURNING ITEM_ID, ITEM_NAME, ITEM_PRICE, STORE_ID""")
        print(query_output)
        json_result = jsonify(query_header,query_output)
        return json_result[0]
    
    @items_blp.arguments(ItemDeleteSchema)
    # @items_blp.response(200,ItemUpdateSchema)
    def delete(self,delete_item_json):
        query_output = db.execute_query(f"""DELETE FROM ITEMS WHERE ITEM_ID = {delete_item_json["item_id"]} RETURNING ITEM_ID, ITEM_NAME, ITEM_PRICE, STORE_ID""")
        if len(query_output) == 0:
            abort(404,"Item not found")
        query_header = ["item_id", "item_name", "item_price" , "store_id"]
        json_result = jsonify(query_header, query_output)
        return json_result
        

