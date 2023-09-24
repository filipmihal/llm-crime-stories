from abc import ABC, abstractmethod
from typing import List

from environment.types import Direction, Location, Position


class GridGenerator(ABC):
    """
    Generates a 2D grid-like environment with Location objects as units of space.
    """
    
    @staticmethod
    def is_in_bounds(current: Position, n_rows: int, n_cols: int) -> bool:
        return 0 <= current.x < n_rows and 0 <= current.y < n_cols
    
    @property
    def relative_directions(self) -> List[Position]:
        return [direction.value for direction in Direction]
    
    @abstractmethod
    def generate(self, size: int, generator_seed: int, debug: bool = False) -> Location:
        pass