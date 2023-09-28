from __future__ import annotations
from enum import Enum
from typing import Dict, List, Optional, Tuple


class Position:
    """
    Wrapper around tuple that represents a position in 2D grid.
    """

    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    def __add__(self, other) -> Position:
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


class Room:
    """
    A unit of space in the crime game.
    """

    def __init__(self):
        self._description = None
        self._name = None
        self._neighbours = {direction.value: None for direction in Direction}

    @property
    def description(self) -> Optional[str]:
        return self._description

    @description.setter
    def description(self, new_description: str) -> None:
        self._description = new_description

    @property
    def name(self) -> Optional[str]:
        return self._name

    @name.setter
    def name(self, new_name: str) -> None:
        self._name = new_name

    @property
    def neighbours(self) -> Dict[Position, Room]:
        return self._neighbours

    @staticmethod
    def connect(start_room: Room, end_room: Room, direction: Position) -> None:
        start_room.neighbours[direction] = end_room
        end_room.neighbours[Direction.opposite(direction)] = start_room

Grid = List[List[Optional[Room]]]

class CrimeSceneMap:
    """
    Represents a map grid of rooms. Encompasses related information.
    """
    
    def __init__(self, number_of_rooms: int):
        self._number_of_rooms = number_of_rooms
        self._rooms = [
            [None] * (2 * number_of_rooms + 1) for _ in range(2 * number_of_rooms + 1)
        ]

    @property
    def number_of_rooms(self) -> int:
        return self._number_of_rooms

    @property
    def rooms(self) -> List[List[Optional[Room]]]:
        return self._rooms

    @property
    def size(self) -> Tuple[int, int]:
        return 2 * self._number_of_rooms + 1, 2 * self._number_of_rooms + 1

    @property
    def start(self) -> Room:
        return self._rooms[self._number_of_rooms][self._number_of_rooms]

    @start.setter
    def start(self, new_start) -> None:
        self._rooms[self._number_of_rooms][self._number_of_rooms] = new_start

    def add_room_to_position(self, row: int, col: int, room: Room) -> None:
        self._rooms[row][col] = room
