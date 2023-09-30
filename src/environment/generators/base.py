from abc import ABC, abstractmethod
from typing import List, Tuple

from environment.types import CrimeSceneMap, Direction, Position


class BaseCrimeSceneMapGenerator(ABC):
    """
    Base class for crime scenes layout generators.
    """

    @property
    def relative_directions(self) -> List[Position]:
        return [direction.value for direction in Direction]

    @staticmethod
    def is_in_bounds(current: Position, size: Tuple[int, int]) -> bool:
        return 0 <= current.x < size[0] and 0 <= current.y < size[1]

    @abstractmethod
    def generate(self, number_of_rooms: int) -> CrimeSceneMap:
        """
        Generates a 2D grid-like environment with Room objects as units of space.
        """
