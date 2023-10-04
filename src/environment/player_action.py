from abc import ABC, abstractmethod
from environment.game_state import GameState
from story.storytelling_context import StorytellingContext
from environment.player.action_result import ActionResult

class PlayerAction(ABC):
    @abstractmethod
    def act(self, game_state: GameState) -> ActionResult:
        pass