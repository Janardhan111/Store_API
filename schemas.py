from marshmallow import Schema, fields

class StoreCreateSchema(Schema):
    name = fields.Str(required=True)
    store_id = fields.Str(dump_only=True)

class StoreUpdateSchema(Schema):
    store_id = fields.Str(required=True)
    name = fields.Str(required=True)

class StoreDeleteSchema(Schema):
    store_id = fields.Str(required=True)

class ItemCreateSchema(Schema):
    name = fields.Str(required=True)
    item_id = fields.Str(dump_only=True)

class ItemUpdateSchema(Schema):
    name = fields.Str(required=True)
    item_id = fields.Str(required=True)

class ItemDeleteSchema(Schema):
    item_id = fields.Str(required=True)