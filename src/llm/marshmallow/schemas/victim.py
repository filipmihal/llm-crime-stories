from marshmallow import Schema, fields, validate, EXCLUDE


class VictimSchema(Schema):
    class Meta:
        unknown = EXCLUDE
    
    name = fields.Str(required=True)
    age = fields.Integer(validate=validate.Range(min=0))
    occupation = fields.Str(required=True)
    murder_weapon = fields.Str(required=True)
    death_description = fields.Str(required=True)
