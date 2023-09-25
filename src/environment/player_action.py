from abc import ABC, abstractmethod
from environment.game_state import GameState

class PlayerAction(ABC):
    @abstractmethod
    def act(self, game_state: GameState) -> bool:
        pass