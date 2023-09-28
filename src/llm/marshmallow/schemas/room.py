from marshmallow import Schema, fields


class RoomSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    row = fields.Integer()
    col = fields.Integer()