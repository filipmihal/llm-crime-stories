from environment.types import Room, Grid, Position
from llm.marshmallow.schemas.suspect import SuspectSchema
from llm.marshmallow.schemas.victim import VictimSchema
from typing import Dict


class GameState:
    def __init__(self, current_location: Room, grid: Grid, dungeon_size: int):
        self._current_room = current_location
        self._previous_room = None
        self._grid = grid
        self._dungeon_size = dungeon_size

    @property
    def victim(self) -> VictimSchema:
        return self._victim

    @victim.setter
    def victim(self, victim: VictimSchema):
        self._victim = victim

    @property
    def suspects(self) -> Dict[Position, SuspectSchema]:
        return self._suspects

    @suspects.setter
    def suspects(self, suspects: Dict[Position, SuspectSchema]):
        self._suspects = suspects

    @property
    def current_room(self) -> Room:
        return self._current_room

    @property
    def dungeon_size(self) -> int:
        return self._dungeon_size

    @property
    def grid(self) -> Grid:
        return self._grid

    @current_room.setter
    def current_room(self, new_room: Room) -> None:
        self._previous_room = self._current_room
        self._current_room = new_room
