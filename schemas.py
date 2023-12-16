from marshmallow import Schema, fields

class StoreCreateSchema(Schema):
    store_name = fields.Str(required=True)
    store_id = fields.Str(dump_only=True)

class StoreUpdateSchema(Schema):
    store_id = fields.Str(required=True)
    store_name = fields.Str(required=True)

class StoreDeleteSchema(Schema):
    store_id = fields.Str(required=True)

class ItemCreateSchema(Schema):
    item_name = fields.Str(required=True)
    item_id = fields.Str(dump_only=True)
    item_price = fields.Str(required=True)
    store_id = fields.Str(required=True)

class ItemUpdateSchema(Schema):
    item_name = fields.Str(required=True)
    item_id = fields.Str(required=True)
    item_price = fields.Str(required=True)
    store_id = fields.Str(required=True)

class ItemDeleteSchema(Schema):
    item_id = fields.Str(required=True)