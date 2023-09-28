from marshmallow import Schema, fields

from llm.marshmallow.schemas.killer import KillerSchema
from llm.marshmallow.schemas.room import RoomSchema
from llm.marshmallow.schemas.suspect import SuspectSchema
from llm.marshmallow.schemas.victim import VictimSchema

class PositionSchema(Schema):
    row = fields.Integer(required=True)
    col = fields.Integer(required=True)

class StorySchema(Schema):
    theme = fields.Str(required=True)
    killer = fields.Nested(KillerSchema)
    victim = fields.Nested(VictimSchema)
    suspects = fields.List(fields.Nested(SuspectSchema))
    rooms = fields.List(fields.Nested(RoomSchema))
    suspects_positions = fields.List(fields.Nested(PositionSchema))
