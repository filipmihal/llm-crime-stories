from environment.game_state import GameState
from environment.player.action_parser import ActionParser
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

    def play(self) -> None:
        print(self._game_state.current_room.description)
        while True:    
            instruction = input("Enter your instruction: ")   
            action = ActionParser.parse(instruction)
            result = action.act(self._game_state)
            if result.terminal:
                if result.win:
                    print("You win!")
                 
                else:
                    print("You lose!")
                return
            if self._visualize:
                GridVisualizer.visualize(self._game_state)

        
