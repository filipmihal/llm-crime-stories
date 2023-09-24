from environment.game import Game
from environment.generators.random_grid_generator import RandomGridGenerator
from environment.grid_visualizer import GridVisualizer
from environment.types import Direction

# Generate a dungeon of the given size.
generator, DUNGEON_SIZE = RandomGridGenerator(), 50
start_location, grid = generator.generate(DUNGEON_SIZE, generator_seed=100, debug=True)

# Visualize.
GridVisualizer.visualize(grid, start_location, DUNGEON_SIZE)

game = Game(start_location)
for c in range(3):
    print("------------------")
    if c % 2 == 0:
        game.move(Direction.NORTH.value)
    else:
        game.move(Direction.EAST.value)
    GridVisualizer.visualize(grid, game.current_location, DUNGEON_SIZE)
