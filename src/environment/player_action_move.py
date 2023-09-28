from environment.player_action import PlayerAction
from environment.game_state import GameState
from environment.types import Position
from story.storytelling_context import StorytellingContext
from story.types import StoryPayload

class PlayerActionMove(PlayerAction):
    def __init__(self, direction: Position):
        self._direction = direction

    def act(self, game_state: GameState) -> None:
        if game_state.current_room.neighbours[self._direction] is None:
            return

        game_state.current_room = game_state.current_room.neighbours[self._direction]