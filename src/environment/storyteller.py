import re
from typing import List, Optional


class Storyteller:
    def __init__(self, atmosphere: List[str], generate_text):
        self._generate_text = generate_text

        self._system_prompt = f'''
            S: You are a storyteller in a text-based game.
            The game has {', '.join(atmosphere)} atmosphere. 
            Your task is to describe locations in a light artistic style.
            There may be or may not be additional descriptive keywords.
            During description process always preserve the atmosphere.
        '''
    
    def tell(self, descriptive_keywords: Optional[List[str]] = None) -> str:
        prompt = self._construct_prompt(descriptive_keywords)
        res = self._generate_text(prompt)
        generated_text = res[0]['generated_text']
        answer = generated_text.split('A:')[1]
        story = re.sub(r'\([^)]*\)', '', answer).strip()
        
        return story
    
    def _construct_prompt(self, descriptive_keywords: Optional[List[str]] = None) -> str:
        if not descriptive_keywords:
            return self._system_prompt + " Q: Describe a new location. A:"
        
        question_prompt = f'''
            Q: Describe a location with these keywords: {', '.join(descriptive_keywords)}.
        '''
        return self._system_prompt + " " + question_prompt + " A:"
        