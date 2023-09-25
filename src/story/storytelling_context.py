from typing import List

from story.storyteller import LlamaStoryteller, SystemStoryteller
from story.types import StoryPayload

class StorytellingContext:
    def __init__(self, atmosphere: List[str]) -> None:
        self._atmosphere = atmosphere
        self._strategies = {
            "llama": LlamaStoryteller(),
            "system": SystemStoryteller()
        }
    
    def describe(self, strategy: str, story_payload: StoryPayload) -> None:
        return self._strategies[strategy].tell(story_payload)