from itertools import product
from typing import Tuple

from environment.types import CrimeSceneMap
from environment.game_state import GameState


class GridVisualizer:
    """
    Visualizes the generated environment.
    """

    @staticmethod
    def get_bounds(crime_scene_map: CrimeSceneMap) -> Tuple[int, int, int, int]:
        top, left, right, bottom = float("inf"), float("inf"), -1, -1
        rows, columns = crime_scene_map.size

        for i, j in product(range(rows), range(columns)):
            if crime_scene_map.rooms[i][j] is not None:
                top = min(top, i)
                left = min(left, j)
                right = max(right, j)
                bottom = max(bottom, i)

        return top, left, right, bottom

    @staticmethod
    def visualize(game_state: GameState) -> None:
        start_location = game_state.current_room
        top, left, right, bottom = GridVisualizer.get_bounds(game_state.crime_scene_map)

        print("------------------")
        for i in range(top, bottom + 1):
            for j in range(left, right + 1):
                if game_state.crime_scene_map.rooms[i][j] is None:
                    print(" ", end="")
                elif game_state.crime_scene_map.rooms[i][j] == start_location:
                    print("X", end="")
                else:
                    print("O", end="")
            print()
        print("------------------")

