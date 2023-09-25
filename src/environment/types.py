from enum import Enum
from typing import Dict, List, Optional


class Position:
    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    def __add__(self, other) -> "Position":
        if isinstance(other, int):
            return Position(self._x + other, self._y + other)

        if isinstance(other, Position):
            return Position(self._x + other.x, self._y + other.y)

        raise TypeError("Unsupported operand type")

    def __eq__(self, other) -> bool:
        if isinstance(other, Position):
            return self._x == other.x and self._y == other._y

        if isinstance(other, tuple) and len(other) == 2:
            return (self._x, self._y) == other

        return False

    def __hash__(self) -> int:
        return hash((self._x, self._y))


class Direction(Enum):
    NORTH = Position(0, -1)
    EAST = Position(1, 0)
    SOUTH = Position(0, 1)
    WEST = Position(-1, 0)

    @staticmethod
    def opposite(direction: Position) -> Position:
        opposites = {
            Direction.NORTH.value: Direction.SOUTH.value,
            Direction.EAST.value: Direction.WEST.value,
        }

        if direction in opposites:
            return opposites[direction]

        return {v: k for k, v in opposites.items()}[direction]


class Location:
    """
    Location class is a unit of space in the dungeon game. It serves as a descriptor for the world.
    """

    def __init__(self):
        self._description = None
        self._neighbours = {direction.value: None for direction in Direction}

    @property
    def description(self) -> str:
        return self._description

    @property.setter
    def description(self, new_description) -> None:
        self._description = new_description

    @property
    def neighbours(self) -> Dict[Position, "Location"]:
        return self._neighbours

    @staticmethod
    def connect(
        location1: "Location", location2: "Location", direction: Position
    ) -> None:
        location1.neighbours[direction] = location2
        location2.neighbours[Direction.opposite(direction)] = location1


Grid = List[List[Optional[Location]]]