from abc import ABC, abstractmethod

from environment.location import Location


class Generator(ABC):
    """
    Generates a 2D grid-like environment with Location objects as units of space.
    """
    
    def __init__(self, number_of_locations: int):
        self._number_of_locations = number_of_locations

    @abstractmethod
    def generate(self) -> Location:
        pass
