from environment.grid_visualizer import GridVisualizer
from environment.generators.random_grid_generator import RandomGridGenerator

# Generate a dungeon of the given size.
generator, DUNGEON_SIZE = RandomGridGenerator(), 10
start_location, grid = generator.generate(DUNGEON_SIZE, debug=True)

# Visualize.
GridVisualizer.visualize(grid, start_location, DUNGEON_SIZE)