from random import choice, seed
from typing import Tuple, Union

from environment.generators.generator import GridGenerator
from environment.types import Grid, Room


class RandomGridGenerator(GridGenerator):

    def __init__(self, dungeon_size: int, seed: int) -> None:
        super().__init__(dungeon_size, seed)

    def generate(self) -> Tuple[Grid, Room]:
        seed(self._seed)
        rows = columns = 2 * self._dungeon_size + 1
        field = [[None] * columns for _ in range(rows)]

        middle = self._dungeon_size
        field[middle][middle] = Room()
        potential_locations = set(
            [direction + middle for direction in self.relative_directions]
        )
        for _ in range(self._dungeon_size-1):
            position = choice(list(potential_locations))
            potential_locations.remove(position)

            new_location = Room()
            field[position.y][position.x] = new_location

            for direction in self.relative_directions:
                new_position = position + direction

                if not GridGenerator.is_in_bounds(new_position, rows, columns):
                    continue

                if not field[new_position.y][new_position.x]:
                    potential_locations.add(new_position)
                else:
                    Room.connect(
                        new_location,
                        field[new_position.y][new_position.x],
                        direction,
                    )

        return field[middle][middle], field
