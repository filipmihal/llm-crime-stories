from marshmallow import Schema, fields, validate


class VictimSchema(Schema):
    name = fields.Str(required=True)
    age = fields.Integer(validate=validate.Range(min=0))
    occupation = fields.Str(required=True)
    murder_weapon = fields.Str(required=True)
    death_description = fields.Str(required=True)
