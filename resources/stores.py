from flask_smorest import Blueprint
from flask.views import MethodView
from flask import request, abort
from uuid import uuid4
from db import stores
from resources.schemas import StoreCreateSchema, StoreUpdateSchema, StoreDeleteSchema

stores_blp = Blueprint("stores",__name__)

@stores_blp.route("/store")
class store(MethodView):

    def get(self):
        return {"stores":stores}

    @stores_blp.arguments(StoreCreateSchema)
    def post(self,store_json):
        store_id = uuid4().hex
        store_json["store_id"] = store_id
        stores[store_id] = store_json
        return store_json

    @stores_blp.arguments(StoreUpdateSchema)
    def put(self,updated_store_json):
        try:
            stores[updated_store_json["store_id"]] |= updated_store_json
        except KeyError as e:
            abort(404,"Item not found")
        else:
            return stores[updated_store_json["store_id"]]

    @stores_blp.arguments(StoreDeleteSchema)
    def delete(self,delete_store_json):
        try:
            deleted_store = stores.pop(store_json["store_id"])
        except:
            abort(404,"Item not found")
        else:
            return deleted_store