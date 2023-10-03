from environment.game_state import GameState
from environment.player_action_parser import PlayerActionParser
from environment.grid_visualizer import GridVisualizer


class Game:
    """
    Game contains the main game logic and the game state.
    """

    def __init__(self, initial_game_state: GameState, visualize: bool = True):
        self._game_state = initial_game_state
        self._visualize = visualize
        
        if visualize:
            GridVisualizer.visualize(self._game_state)

    def play(self, instruction_text: str = None) -> None:
        instructions = PlayerActionParser.parse_raw(instruction_text)
        # for instruction in instructions:
        while True:    
            instruction = input("Enter your instruction: ")   
            action = PlayerActionParser.parse(instruction)
            if action is not None:
                action.act(self._game_state)
            else:
                # TODO: maybe write something better here?
                print("Invalid instruction: " + instruction)
            if self._visualize:
                print("------------------")
                GridVisualizer.visualize(self._game_state)
        
