from typing import List, Optional

from story.storyteller import Storyteller
from story.types import StoryPayload

class StorytellingContext:
    def __init__(self, atmosphere: List[str], strategy: Optional[Storyteller] = None) -> None:
        self._atmosphere = atmosphere
        self._strategy = strategy
        
    @property
    def strategy(self) -> Storyteller:
        return self._strategy
    
    @property.setter
    def strategy(self, new_strategy: Storyteller) -> None:
        self._strategy = new_strategy
        
    def describe(self, game_state) -> None:   
        # game_state.error + message if there is
        
        # prepare payload
        story_payload = StoryPayload(self._atmosphere, error=...)
                
        return self._strategy.tell(story_payload)