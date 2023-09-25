from environment.player_action import PlayerAction
from environment.game_state import GameState
from environment.types import Position
from story.storytelling_context import StorytellingContext
from story.types import StoryPayload

class PlayerActionMove(PlayerAction):
    def __init__(self, direction: Position):
        self._direction = direction

    def act(self, game_state: GameState, storytelling_context: StorytellingContext) -> None:
        if game_state.current_location.neighbours[self._direction] is None:
            print(storytelling_context.describe("system", StoryPayload(error="Not valid move.")))
            return

        game_state.current_location = game_state.current_location.neighbours[self._direction]
        if game_state.current_location.description:
            print(storytelling_context.describe("system", StoryPayload(text=game_state.current_location.description)))
            return
        
        location_description = storytelling_context.describe("llama", StoryPayload(atmosphere=game_state.atmosphere))
        game_state.current_location.description = location_description
        print(location_description)