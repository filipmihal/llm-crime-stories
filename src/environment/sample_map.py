from environment.generators.random_generator import RandomCrimeSceneMapGenerator
from environment.game_state import GameState
import json

class SampleMap:
    @staticmethod
    def load_story():
        number_of_rooms = 5
        crime_scene_map = RandomCrimeSceneMapGenerator().generate(number_of_rooms, 42)
        json_path = 'data/Smallville_Clark_Kent_2010.json'
        with open(json_path, 'r') as file:
            story = json.load(file)
            return GameState(crime_scene_map, story)

        