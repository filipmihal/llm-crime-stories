from environment.types import Location, Position
from environment.game_state import GameState
from environment.player_action_parser import PlayerActionParser
from environment.grid_visualizer import GridVisualizer
from environment.generators.generator import GridGenerator

class Game:
    """
    Game contains the main game logic and the game state.
    """

    def __init__(self, generator: GridGenerator):
        start_location, grid = generator.generate()
        self._game_state = GameState(start_location, grid, generator.dungeon_size)
    
    def play(self, instruction_text: str, visualize: bool = True) -> None:
        GridVisualizer.visualize(self._game_state)
        instructions = PlayerActionParser.parse_raw(instruction_text)
        for instruction in instructions:
            action = PlayerActionParser.parse(instruction)
            if action is not None:
                action.act(self._game_state)
            else:
                # TODO: maybe write something better here?
                print("Invalid instruction: " + instruction)
            if visualize:
                GridVisualizer.visualize(self._game_state)
                
        

        

