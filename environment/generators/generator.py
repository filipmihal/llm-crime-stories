"""
Generates a 2D grid-like environment with Location objects as units of space.
"""

from ..location import Location
from abc import ABC, abstractmethod
 

class Generator:
    def __init__(self, number_of_locations: int):
        self.number_of_locations = number_of_locations
    
    @abstractmethod
    def generate(self) -> Location:
        pass