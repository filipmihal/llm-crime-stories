from random import choice
from typing import Tuple, Union

from environment.generators.generator import GridGenerator
from environment.types import Grid, Location

class RandomGridGenerator(GridGenerator):
    def generate(self, size: int, debug: bool = False) -> Union[Tuple[Grid, Location], Location]:
        rows = columns = 2 * size + 1
        field = [[None] * columns for _ in range(rows)]

        middle = size
        field[middle][middle] = Location()
        potential_locations = set([direction + middle for direction in self.relative_directions])
        for _ in range(size):
            position = choice(list(potential_locations))
            potential_locations.remove(position)
            
            new_location = Location()
            field[position.x][position.y] = new_location

            for direction in self.relative_directions:
                new_position = position + direction
                
                if not GridGenerator.is_in_bounds(new_position, rows, columns):
                    continue
                
                if not field[new_position.x][new_position.y]:
                    potential_locations.add(new_position)
                else:
                    Location.connect(
                        new_location,
                        field[new_position.x][new_position.y],
                        direction,
                    )
        
        return field[middle][middle], field if debug else field[middle][middle]
