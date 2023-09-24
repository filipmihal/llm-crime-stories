from environment.types import Grid, Location
from typing import Tuple

class GridVisualizer:
    """
    Visualizes the generated environment.
    """

    @staticmethod
    def get_top_bound(grid: Grid, size: int) -> int:
        rows = columns = 2 * size + 1
        for i in range(rows):
            for j in range(columns):
                if grid[i][j] is not None:
                    return i
    
    @staticmethod
    def get_left_bound(grid: Grid, size: int) -> int:
        rows = columns = 2 * size + 1
        for j in range(columns):
            for i in range(rows):
                if grid[i][j] is not None:
                    return j
    
    @staticmethod
    def get_right_bound(grid: Grid, size: int) -> int:
        rows = columns = 2 * size + 1
        for j in range(columns - 1, -1, -1):
            for i in range(rows):
                if grid[i][j] is not None:
                    return j
    
    @staticmethod
    def get_bottom_bound(grid: Grid, size: int) -> int:
        rows = columns = 2 * size + 1
        for i in range(rows - 1, -1, -1):
            for j in range(columns):
                if grid[i][j] is not None:
                    return i
    
    @staticmethod
    def visualize(grid: Grid, start_location: Location, size: int) -> None:
        top = GridVisualizer.get_top_bound(grid, size)
        left = GridVisualizer.get_left_bound(grid, size)
        right = GridVisualizer.get_right_bound(grid, size)
        bottom = GridVisualizer.get_bottom_bound(grid, size)

        for i in range(top, bottom + 1):
            for j in range(left, right + 1):
                if grid[i][j] is None:
                    print(' ', end='')
                elif grid[i][j] == start_location:
                    print('X', end='')
                else:
                    print('O', end='')
            print()
