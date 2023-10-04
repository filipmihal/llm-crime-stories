from environment.player_action import PlayerAction
from environment.game_state import GameState
from environment.types import Position
from environment.player.action_result import ActionResult

class PlayerActionMove(PlayerAction):
    def __init__(self, direction: Position):
        self._direction = direction

    def act(self, game_state: GameState) -> ActionResult:
        if game_state.current_room.neighbours[self._direction] is None:
            print("You can't go that way")
            return ActionResult(False, False)

        game_state.current_room = game_state.current_room.neighbours[self._direction]
        print(game_state.current_room.description)
        return ActionResult(False, False)