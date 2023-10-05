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
            for dir_enum in Direction:
                if dir_enum.name == direction_text.upper():
                    return ActionMove(dir_enum.value)
        elif action == "accuse":
            return ActionAccuse()
    
        return ActionInvalid()
    
    @staticmethod
    def parse_raw(text: str) -> List[str]:
        return text.split("\n")