from flask_smorest import Blueprint
from flask.views import MethodView
from schemas import ItemCreateSchema, ItemUpdateSchema, ItemDeleteSchema
from flask import abort
from uuid import uuid4
from db import items

items_blp = Blueprint("items",__name__)

@items_blp.route("/items")
class item(MethodView):
    @items_blp.response(200,ItemUpdateSchema(many=True))
    def get(self):
        return items.values()

    @items_blp.arguments(ItemCreateSchema)
    @items_blp.response(200,ItemUpdateSchema)
    def post(self,item_json):
        item_id = uuid4().hex
        item_json["item_id"] = item_id
        items[item_id] = item_json
        return items[item_id]

    @items_blp.arguments(ItemUpdateSchema)
    @items_blp.response(200,ItemUpdateSchema)
    def put(self,updated_item_json):
        if updated_item_json["item_id"] not in items.keys():
            abort(404,"Item not found")
        items[updated_item_json["item_id"]] = updated_item_json
        return items[updated_item_json["item_id"]]
    
    @items_blp.arguments(ItemDeleteSchema)
    @items_blp.response(200,ItemUpdateSchema)
    def delete(self,delete_item_json):
        try:
            deleted_item = items.pop(delete_item_json["item_id"])
        except KeyError as e:
            abort(404,"Item not found")
        else:
            return deleted_item

