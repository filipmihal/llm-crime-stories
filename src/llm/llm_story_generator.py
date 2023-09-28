from dataclasses import dataclass
import json
from typing import List
from environment.types import Position

@dataclass
class SchemaRoom:
    name: str
    description: str
    row: int
    col: int

@dataclass
class SchemaSuspect:
    name: str
    age: int
    occupation: str
    is_guilty: bool
    motive: str
    alibi: str
 

@dataclass
class SchemaVictim:
    name: str
    age: int
    occupation: str
    murder_weapon: str
    death_description: str

@dataclass
class SchemaStory:
    theme: str
    victim: SchemaVictim
    suspects: List[SchemaSuspect]
    rooms: List[SchemaRoom]
    suspects_positions: List[Position]

class LlmStoryGenerator:
    def __init__(self):
        pass
    
    def create_new_story(self, dummy: bool = False) -> SchemaStory:
        if dummy:
            with open("./llm-dungeon-adventures/data/dummy.json", 'r') as f:
                return json.load(f)
    
        # complex llm logic with langchain
    
        return {}