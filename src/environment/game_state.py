from environment.types import Room, Grid, Position
from llm.llm_story_generator import SchemaSuspect, SchemaVictim
from typing import List, Dict


class GameState:
    def __init__(self,current_location: Room, grid: Grid, dungeon_size: int):
        self._current_room = current_location
        self._previous_room = None
        self._grid = grid
        self._dungeon_size = dungeon_size

    @property
    def victim(self) -> SchemaVictim:
        return self._victim
    
    @victim.setter
    def victim(self, victim: SchemaVictim):
        self._victim = victim
    
    @property
    def suspects(self) ->Dict[Position, SchemaSuspect]:
        return self._suspects
    
    @suspects.setter
    def suspects(self, suspects: Dict[Position, SchemaSuspect]):
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
    def current_room(self, new_room: Room):
        self._previous_room = self._current_room
        self._current_room = new_room
    
