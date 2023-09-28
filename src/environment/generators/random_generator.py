from random import choice, seed as random_seed

from environment.generators.base import BaseCrimeSceneMapGenerator
from environment.types import CrimeSceneMap, Room


class RandomCrimeSceneMapGenerator(BaseCrimeSceneMapGenerator):
    def generate(self, number_of_rooms: int, seed: int) -> CrimeSceneMap:
        random_seed(seed)
        middle = number_of_rooms

        map = CrimeSceneMap(number_of_rooms)
        map.start = Room()
        potential_locations = set(
            [direction + middle for direction in self.relative_directions]
        )
        for _ in range(number_of_rooms - 1):
            position = choice(list(potential_locations))
            potential_locations.remove(position)

            map.add_room_to_position(position.x, position.y, Room())

            for direction in self.relative_directions:
                new_position = position + direction

                if not BaseCrimeSceneMapGenerator.is_in_bounds(new_position, map.size):
                    continue

                if not map.rooms[new_position.y][new_position.x]:
                    potential_locations.add(new_position)
                else:
                    Room.connect(
                        map.rooms[position.y][position.x],
                        map.rooms[new_position.y][new_position.x],
                        direction,
                    )

        return map
