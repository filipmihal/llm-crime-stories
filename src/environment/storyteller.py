from abc import abstractmethod
import re

from llm.llama import Llama
from llm.types import StoryContext

class Storyteller:
    """
    Describe an entity that will guide a player throughout a story.
    """
    
    @abstractmethod
    def tell(self, context: StoryContext) -> str:
        """
        Returns a few light artistic sentences describing an atmosphere in a location.
        """

class LlamaStoryteller(Storyteller):
    def __init__(self):
        self._question_prompt = f"""
            Q: Describe a new location's atmosphere.
        """

        self._system_prompt = lambda atmosphere: f"""
            S: You are a storyteller in a text-based game.
            The game has this specific general atmosphere: {', '.join(atmosphere)}.
            Your task is to describe location atmosphere in a light artistic style using 2-3 sentences.
        """
        
        self._llama = Llama()
        
    def tell(self, context: StoryContext) -> str:
        # Construct prompt.
        prompt = self._system_prompt(context.atmosphere) + " " + self._question_prompt + " A:"
        
        # Run inference pipeline.
        res = self._llama.generate_text(prompt)
        
        # Parse the answer out of the returned context.
        generated_text = res[0]["generated_text"]
        answer = generated_text.split("A:")[1]
        story = re.sub(r"\([^)]*\)", "", answer).strip()

        return story
        
class SystemStoryteller(Storyteller):
    """
    Acts as a dummy storyteller that just returns the system prompts e.g. errors like when wrong direction was specified.
    """
    
    def tell(self, context: StoryContext) -> str:
        return context.error