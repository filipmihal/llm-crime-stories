from marshmallow import Schema, fields, EXCLUDE


class RoomSchema(Schema):
    class Meta:
        unknown = EXCLUDE
    
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    row = fields.Integer()
    col = fields.Integer()