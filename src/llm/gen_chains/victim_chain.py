import json
from langchain.prompts import PromptTemplate

from llm.gen_chains.json_output_parser import JsonOutputParser


class VictimChain:
    def __init__(self, llm):
        self._prompt = PromptTemplate.from_template(
            """
            <s>[INST] <<SYS>>
            You are a crime storyteller. The theme of the story is: {{theme}}. No pre-amble.
            <<SYS>>

            Describe a victim's name, age, occupation, murder weapon and death description. Output is according to this Python class:
            class Victim:
                name: str
                age: int
                occupation: str
                murder_weapon: str
                death_description: str
            """
        )

        self._chain = self._prompt | llm | JsonOutputParser()

    def create(self, theme):
        return self._chain.invoke({"theme": theme})
