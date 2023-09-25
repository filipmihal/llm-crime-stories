from abc import ABC, abstractmethod
from typing import List, Tuple

from environment.types import Direction, Location, Position, Grid


class GridGenerator(ABC):
    """
    Generates a 2D grid-like environment with Location objects as units of space.
    """

    def __init__(self, dungeon_size: int, seed: int) -> None:
        self._dungeon_size = dungeon_size
        self._seed = seed

    @property
    def dungeon_size(self) -> int:
        return self._dungeon_size
    

    @staticmethod
    def is_in_bounds(current: Position, n_rows: int, n_cols: int) -> bool:
        return 0 <= current.x < n_rows and 0 <= current.y < n_cols

    @property
    def relative_directions(self) -> List[Position]:
        return [direction.value for direction in Direction]

    @abstractmethod
    def generate(self, size: int, generator_seed: int) -> Tuple[Location, Grid]:
        pass
