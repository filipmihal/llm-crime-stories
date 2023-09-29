from marshmallow import Schema, fields, validate, EXCLUDE


class KillerSchema(Schema):
    class Meta:
        unknown = EXCLUDE
    
    name = fields.Str(required=True)
    age = fields.Integer(required=True, validate=validate.Range(min=0))
    occupation = fields.Str(required=True)
    alibi = fields.Str(required=True)
