from abc import abstractmethod, ABC
import re

from llm.llama import Llama
from story.types import StoryPayload

class Storyteller(ABC):
    """
    Describe an entity that will guide a player throughout a story.
    Acts as a strategy in storytelling.
    """
    
    @abstractmethod
    def tell(self, story_payload: StoryPayload) -> str:
        """
        Returns a few light artistic sentences describing an atmosphere in a location.
        """

class LlamaStoryteller(Storyteller):
    """
    Llama-based guiding entity strategy.
    """
    
    def __init__(self) -> None:
        self._question_prompt = f"""
            Q: Create a new location and describe its atmosphere.
        """

        self._system_prompt = lambda atmosphere: f"""
            S: You are a storyteller in a text-based game.
            The game has this general atmosphere: {', '.join(atmosphere)}.
            Your task is to create new locations and describe their atmosphere in a light artistic style using 2-3 sentences while maintaining the general atmosphere.
        """
        
        self._llama = Llama()
    
    def tell(self, story_payload: StoryPayload) -> str:
        # Construct prompt.
        prompt = self._system_prompt(story_payload.atmosphere) + " " + self._question_prompt + " A:"
        
        # Run inference pipeline.
        res = self._llama.generate_text(prompt)
        
        # Parse the answer out of the returned context.
        generated_text = res[0]["generated_text"]
        answer = generated_text.split("A:")[1]
        story = re.sub(r"\([^)]*\)", "", answer).strip()

        return story

class SystemStoryteller(Storyteller):
    """
    Acts as a dummy storyteller strategy that just returns the system prompts.
    For example, errors like when wrong direction was specified.
    """
    
    def tell(self, story_payload: StoryPayload) -> str:
        return story_payload.error or story_payload.text