from typing import Optional, List
from environment.types import Direction
from environment.player_action import PlayerAction
from environment.player_action_move import PlayerActionMove

class PlayerActionParser():
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
                return PlayerActionMove(direction)
        return None
    
    @staticmethod
    def parse_raw(text: str) -> List[str]:
        return text.split("\n")