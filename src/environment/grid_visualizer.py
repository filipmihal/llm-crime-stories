from itertools import product
from typing import Tuple

from environment.types import Grid
from environment.game_state import GameState


class GridVisualizer:
    """
    Visualizes the generated environment.
    """

    @staticmethod
    def get_bounds(grid: Grid, size: int) -> Tuple[int, int, int, int]:
        top, left, right, bottom = float("inf"), float("inf"), -1, -1
        rows = columns = 2 * size + 1

        for i, j in product(range(rows), range(columns)):
            if grid[i][j] is not None:
                top = min(top, i)
                left = min(left, j)
                right = max(right, j)
                bottom = max(bottom, i)

        return top, left, right, bottom

    @staticmethod
    def visualize(game_state: GameState) -> None:
        start_location = game_state.current_location
        grid = game_state.grid
        top, left, right, bottom = GridVisualizer.get_bounds(grid, game_state.dungeon_size)

        for i in range(top, bottom + 1):
            for j in range(left, right + 1):
                if grid[i][j] is None:
                    print(" ", end="")
                elif grid[i][j] == start_location:
                    print("X", end="")
                else:
                    print("O", end="")
            print()
