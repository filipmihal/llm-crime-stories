from environment.player_action import PlayerAction
from environment.game_state import GameState
from environment.types import Position

class PlayerActionInvalid(PlayerAction):
    def __init__(self, direction: Position):
        self._direction = direction

    def act(self) -> None:
        print("Invalid instruction")