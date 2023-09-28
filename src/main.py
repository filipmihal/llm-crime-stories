from environment.game import Game
from environment.generators.random_generator import RandomGridGenerator
from environment.types import Position
from llm.llm_story_generator import SchemaStory, SchemaVictim, SchemaSuspect, SchemaRoom
import json

# This seed is the exact match for dummy data
generator = RandomGridGenerator(4, 152)
game = Game(generator)

with open('data/dummy.json', "r") as f:
    data = json.load(f)
    victim_json = data['victim']
    victim = SchemaVictim(victim_json['name'], victim_json['age'],victim_json['occupation'], victim_json['death_description'], victim_json['death_description'])
    suspects = []
    for suspect in data['suspects']:
        suspects.append(SchemaSuspect(suspect['name'], suspect['age'], suspect['occupation'], suspect['is_guilty'], suspect['motive'], suspect['alibi']))
    rooms = []
    for room in data['rooms']:
        rooms.append(SchemaRoom(room['name'], room['description'], room['row'], room['col']))
    suspects_positions = [Position(suspect['row'], suspect['col']) for suspect in data['suspects_positions']]
    schema = SchemaStory(data['theme'], victim, suspects, rooms, suspects_positions)
    game.import_story(schema)

