from abc import ABC, abstractmethod
from environment.game_state import GameState
from story.storytelling_context import StorytellingContext

class PlayerAction(ABC):
    @abstractmethod
    def act(self, game_state: GameState) -> None:
        pass