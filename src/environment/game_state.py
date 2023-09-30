from typing import Dict

from environment.types import CrimeSceneMap, Position, Room
from llm.marshmallow.schemas.story import StorySchema
from llm.marshmallow.schemas.suspect import SuspectSchema
from llm.marshmallow.schemas.victim import VictimSchema

class GameState:
    def __init__(self, crime_scene_map: CrimeSceneMap, story: StorySchema) -> None:
        self._crime_scene_map = crime_scene_map
        self._current_room, self._previous_room = crime_scene_map.start, None
        
        self._import_story(story)

    @property
    def crime_scene_map(self) -> CrimeSceneMap:
        return self.crime_scene_map

    @property
    def current_room(self) -> Room:
        return self._current_room

    @current_room.setter
    def current_room(self, new_room: Room) -> None:
        self._previous_room = self._current_room
        self._current_room = new_room

    @property
    def suspects(self) -> Dict[Position, SuspectSchema]:
        return self._suspects

    @property
    def victim(self) -> VictimSchema:
        return self._victim

    def _import_story(self, story: StorySchema) -> None:
        self._victim = story["victim"]
        
        self._suspects = {}
        for suspect, position in zip(story["suspects"] + [story["killer"]], story["suspects_positions"]):
            self._suspects[Position(position["row"], position["col"])] = suspect
        
        for room in story["rooms"]:
            self._crime_scene_map.rooms[room["row"]][room["col"]].name = room["name"]
            self._crime_scene_map.rooms[room["row"]][room["col"]].description = room["description"]