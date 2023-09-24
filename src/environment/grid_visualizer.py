from environment.types import Grid, Location
from typing import Tuple

class GridVisualizer:
    """
    Visualizes the generated environment.
    """

    @staticmethod
    def get_bounds(grid: Grid, size: int) -> (int, int, int, int):
        top, left, right, bottom = float('inf'), float('inf'), -1, -1

        for i in range(2 * size + 1):
            for j in range(2 * size + 1):
                if grid[i][j] is not None:
                    top = min(top, i)
                    left = min(left, j)
                    right = max(right, j)
                    bottom = max(bottom, i)

        return top, left, right, bottom
    
    @staticmethod
    def visualize(grid: Grid, start_location: Location, size: int) -> None:
        top, left, right, bottom = GridVisualizer.get_bounds(grid, size)

        for i in range(top, bottom + 1):
            for j in range(left, right + 1):
                if grid[i][j] is None:
                    print(' ', end='')
                elif grid[i][j] == start_location:
                    print('X', end='')
                else:
                    print('O', end='')
            print()
