from environment.sample_map import SampleMap
from environment.game import Game

game_state = SampleMap.load_story()
game = Game(game_state)
game.play()
