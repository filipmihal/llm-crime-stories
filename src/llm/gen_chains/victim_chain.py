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

            Describe a victim's name, age, occupation, murder weapon and death description. Output it as YAML.
                
            For example, if you describe a victim like Alicia Williams, 25 years, nurse, killed by a hunter's knife, stabbed 36 times in the guts.
            Then your desired output is:
            ```
            victim:
                name: "Alicia Williams"
                age: 25
                occupation: "nurse"
                murder_weapon: "hunter's knife"
                death_description: "Body lying in blood on the kitchen's floor, stabbed 36 times in the body area"
            ```
            """
        )

        self._chain = self._prompt | llm | JsonOutputParser()

    def create(self, theme):
        return self._chain.invoke({"theme": theme})
