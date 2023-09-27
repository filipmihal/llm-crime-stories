from dataclasses import dataclass
import json
from typing import List

@dataclass
class Room:
    name: str
    description: str

@dataclass
class Suspect:
    name: str
    age: int
    occupation: str
    is_guilty: bool
    motive: str
    alibi: str

@dataclass
class Victim:
    name: str
    age: int
    occupation: str
    murder_weapon: str
    death_description: str

@dataclass
class Story:
    theme: str
    victim: Victim
    suspects: List[Suspect]
    rooms: List[Room]

class LlmStoryGenerator:
    def __init__(self):
        pass
    
    def create_new_story(self, dummy: bool = False) -> Story:
        if dummy:
            with open("./llm-dungeon-adventures/data/dummy.json", 'r') as f:
                return json.load(f)
    
        # complex llm logic with langchain
    
        return {}