from random import choice

from environment.location import Location
from environment.generators.generator import Generator


class GridGenerator(Generator):
    """
    Generates a 2D grid-like environment with Location objects as units of space.
    """

    def __init__(self, number_of_locations: int):
        super().__init__(number_of_locations)
        self.generate()

    def generate(self) -> Location:
        rows = 2 * self.number_of_locations + 1
        columns = 2 * self.number_of_locations + 1
        self.field = [[None] * columns for _ in range(rows)]

        middle = self.number_of_locations
        self.field[middle][middle] = Location()
        self.starting_location = self.field[middle][middle]
        relative_directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        potential_locations = set(
            [
                (middle + direction[0], middle + direction[1])
                for direction in relative_directions
            ]
        )
        for _ in range(self.number_of_locations):
            new_locations = Location()
            new_position = choice(potential_locations)
            potential_locations.remove(new_position)
            self.field[new_position[0]][new_position[1]] = new_locations

            for direction in relative_directions:
                if not (
                    0 <= new_position[0] + direction[0] < rows
                    and 0 <= new_position[1] + direction[1] < columns
                ):
                    continue
                if (
                    self.field[new_position[0] + direction[0]][
                        new_position[1] + direction[1]
                    ]
                    is None
                ):
                    potential_locations.add(
                        (new_position[0] + direction[0], new_position[1] + direction[1])
                    )
                else:
                    world_direction = ""
                    if new_position[0] == 0 and new_position[1] == -1:
                        world_direction = "north"
                    elif new_position[0] == 0 and new_position[1] == 1:
                        world_direction = "south"
                    elif new_position[0] == -1 and new_position[1] == 0:
                        world_direction = "west"
                    elif new_position[0] == 1 and new_position[1] == 0:
                        world_direction = "east"

                    Location.connect(
                        new_locations,
                        self.field[new_position[0] + direction[0]][
                            new_position[1] + direction[1]
                        ],
                        world_direction,
                    )

        return self.field[middle][middle]

    def visualize(self) -> None:
        """
        Visualizes the generated environment.
        """
        rows = 2 * self.number_of_locations + 1
        columns = 2 * self.number_of_locations + 1
        for i in range(rows):
            for j in range(columns):
                if self.field[i][j] is None:
                    print(" ", end="")
                elif self.field[i][j] == self.starting_location:
                    print("X", end="")
                else:
                    print("O", end="")
            print()
