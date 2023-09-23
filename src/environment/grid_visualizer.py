from environment.types import Grid, Location

class GridVisualizer:
    """
    Visualizes the generated environment.
    """
    
    @staticmethod
    def visualize(grid: Grid, start_location: Location, size: int) -> None:
        rows = columns = 2 * size + 1
        for i in range(rows):
            for j in range(columns):
                if grid[i][j] is None:
                    print(" ", end="")
                elif grid[i][j] == start_location:
                    print("X", end="")
                else:
                    print("O", end="")
            print()