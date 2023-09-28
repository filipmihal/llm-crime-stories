from environment.game_state import GameState
from environment.player_action_parser import PlayerActionParser
from environment.grid_visualizer import GridVisualizer
from environment.generators.generator import GridGenerator
from llm.llm_story_generator import SchemaStory

class Game:
    """
    Game contains the main game logic and the game state.
    """

    def __init__(self, generator: GridGenerator, visualize: bool = True):
        start_location, grid = generator.generate()
        self._game_state = GameState(start_location, grid, generator.dungeon_size)
        self._visualize = visualize
        if visualize:
            GridVisualizer.visualize(self._game_state)
    
    def play(self, instruction_text: str) -> None:
        instructions = PlayerActionParser.parse_raw(instruction_text)
        for instruction in instructions:
            action = PlayerActionParser.parse(instruction)
            if action is not None:
                action.act(self._game_state)
            else:
                # TODO: maybe write something better here?
                print("Invalid instruction: " + instruction)
            if self._visualize:
                print('------------------')
                GridVisualizer.visualize(self._game_state)
    
    def import_story(self, story: SchemaStory) -> None:
        self._game_state.victim = story.victim
        suspects = {}
        for suspect, position in zip(story.suspects, story.suspects_positions):
            suspects[position] = suspect
        self._game_state.suspects = suspects
        for room in story.rooms:
            self._game_state.grid[room.row][room.col].name = room.name
            self._game_state.grid[room.row][room.col].description = room.description
        
    



                
        

        

