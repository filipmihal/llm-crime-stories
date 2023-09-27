from langchain.prompts import PromptTemplate

from llm.gen_chains.json_output_parser import JsonOutputParser


class VictimChain:
    def __init__(self, llm):
        self._json_schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "title": "Generated schema for Root",
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

        self._prompt = PromptTemplate.from_template(
            """
            You are a crime storyteller. The theme of the story is: {{theme}}.
            Describe a victim and a murder weapon. Return the response in this json schema: {{schema}}
        """
        )
        self._chain = self._prompt | llm | JsonOutputParser()

    def create(self, theme):
        return self._chain.invoke({"theme": theme, "schema": self._schema})
