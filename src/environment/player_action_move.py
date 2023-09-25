from environment.player_action import PlayerAction
from environment.game_state import GameState
from environment.types import Position

class PlayerActionMove(PlayerAction):
    def __init__(self, direction: Position):
        self._direction = direction

    def act(self, game_state: GameState) -> bool:
        if game_state.current_location.neighbours[self._direction] is None:
            return False

        game_state.current_location = game_state.current_location.neighbours[self._direction]

        return True