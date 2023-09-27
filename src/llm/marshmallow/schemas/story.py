from marshmallow import Schema, fields

from llm.marshmallow.schemas import (
    KillerSchema,
    RoomSchema,
    SuspectSchema,
    VictimSchema
)

class StorySchema(Schema):
    theme = fields.Str(required=True)
    killer = fields.Nested(KillerSchema)
    victim = fields.Nested(VictimSchema)
    suspects = fields.List(fields.Nested(SuspectSchema))
    rooms = fields.List(fields.Nested(RoomSchema))
    suspects_positions = fields.List(fields.Tuple(fields.Integer(), fields.Integer()))
