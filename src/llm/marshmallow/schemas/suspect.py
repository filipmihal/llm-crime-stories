from marshmallow import Schema, fields, validate


class SuspectSchema(Schema):
    name = fields.Str(required=True)
    age = fields.Integer(validate=validate.Range(min=0))
    occupation = fields.Str(required=True)
    motive = fields.Str(required=True)
    alibi = fields.Str(required=True)
