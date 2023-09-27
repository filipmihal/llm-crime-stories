import json
from langchain.prompts import PromptTemplate

from llm.gen_chains.json_output_parser import JsonOutputParser


class SuspectChain:
    def __init__(self, llm):
        self._json_schema = json.dump(
            {
                "$schema": "http://json-schema.org/draft-07/schema#",
                "title": "Generated schema for Root",
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "age": {"type": "number"},
                    "occupation": {"type": "string"},
                    "alibi": {"type": "string"},
                    "motivation": {"type": "string"},
                    "is_guilty": {"type": "boolean"},
                },
                "required": [
                    "name",
                    "age",
                    "occupation",
                    "alibi",
                    "motivation",
                    "is_guilty",
                ],
            }
        )

        self._prompt = PromptTemplate.from_template(
            """
            You are a crime storyteller. The theme of the story is: {{theme}}.
            The victim: {{victim}}. Describe 3 suspects, one of whom is the killer.
            Return the response in this json schema: {{schema}}
        """
        )

        self._chain = self._prompt | llm | JsonOutputParser()

    def create(self, theme, victim):
        return self._chain.invoke(
            {"theme": theme, "victim": victim, "schema": self._json_schema}
        )
