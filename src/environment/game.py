from environment.game_state import GameState
from environment.player_action_parser import PlayerActionParser
from environment.grid_visualizer import GridVisualizer
from environment.generators.generator import GridGenerator
from story.storytelling_context import StorytellingContext
from story.storyteller import SystemStoryteller
from story.types import StoryPayload

from typing import List

class Game:
    """
    Game contains the main game logic and the game state.
    """

    def __init__(self, generator: GridGenerator, atmosphere: List[str]) -> None:
        start_location, grid = generator.generate()
        self._game_state = GameState(atmosphere, start_location, grid, generator.dungeon_size)
        self._storytelling_context = StorytellingContext(atmosphere)
    
    def play(self, instruction_text: str, visualize: bool = True) -> None:
        if visualize:
            GridVisualizer.visualize(self._game_state)
        
        instructions = PlayerActionParser.parse_raw(instruction_text)
        for instruction in instructions:
            action = PlayerActionParser.parse(instruction)
            if not action:
                self._storytelling_context.describe("system", StoryPayload(error="Invalid instruction: " + instruction))
                continue
            
            action.act(self._game_state, self._storytelling_context)
                       
            if visualize:
                GridVisualizer.visualize(self._game_state)
                
        

        

