from marshmallow import Schema, fields

class StoreCreateSchema(Schema):
    store_name = fields.Str(required=True)
class PlaneStoreSchema(Schema):
    store_id = fields.Str(required=True)
    store_name = fields.Str(required=True)

class ItemCreateSchema(Schema):
    item_name = fields.Str(required=True)
    item_price = fields.Str(required=True)
    store_id = fields.Str(required=True)

class PlaneItemSchema(Schema):
    item_name = fields.Str(required=True)
    item_id = fields.Str(required=True)
    item_price = fields.Str(required=True)
    store_id = fields.Str(required=True)

class ItemSchema(PlaneItemSchema):
    store = fields.Nested(PlaneStoreSchema(),required=True)

class StoreSchema(Schema):
    store_id = fields.Str(required=True)
    store_name = fields.Str(required=True)
    items = fields.List(fields.Nested(ItemSchema()),required=True)