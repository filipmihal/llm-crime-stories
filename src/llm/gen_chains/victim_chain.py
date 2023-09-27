import json
from langchain.prompts import PromptTemplate

from llm.gen_chains.json_output_parser import JsonOutputParser


class VictimChain:
    def __init__(self, llm):
        self._json_schema = json.dumps(
            {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "age": {"type": "number"},
                    "occupation": {"type": "string"},
                    "murder_weapon": {"type": "string"},
                    "death_description": {"type": "string"},
                },
                "required": [
                    "name",
                    "age",
                    "occupation",
                    "murder_weapon",
                    "death_description",
                ],
            }
        )

        self._prompt = PromptTemplate.from_template(
            """
            <s>[INST] <<SYS>>
            You are a crime storyteller.
            Always output your answer in JSON according to the schema {{schema}}.
            No pre-amble.
            The theme of the story is: {{theme}}.
            <<SYS>>

            Describe a victim and a murder weapon. [/INST]
            """
        )

        self._chain = self._prompt | llm | JsonOutputParser()

    def create(self, theme):
        return self._chain.invoke({"theme": theme, "schema": self._json_schema})
