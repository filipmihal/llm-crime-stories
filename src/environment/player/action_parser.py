from typing import Optional, List
from environment.types import Direction
from environment.player_action import PlayerAction
from environment.player.action_move import ActionMove
from environment.player.action_invalid import ActionInvalid
from environment.player.action_accuse import ActionAccuse

class ActionParser():
    @staticmethod
    def parse(action: str) -> Optional[PlayerAction]:
        if action.startswith("go"):
            direction_text = action.split(" ")[1]
            direction = None
            if direction_text == "north":
                direction = Direction.NORTH.value
            elif direction_text == "east":
                direction = Direction.EAST.value
            elif direction_text == "south":
                direction = Direction.SOUTH.value
            elif direction_text == "west":
                direction = Direction.WEST.value
            
            if direction is not None:
                return ActionMove(direction)
        if action == "accuse":
            return ActionAccuse()
    
        return ActionInvalid()
    
    @staticmethod
    def parse_raw(text: str) -> List[str]:
        return text.split("\n")