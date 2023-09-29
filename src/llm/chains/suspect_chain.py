import json
from langchain.prompts import PromptTemplate

from llm.output_parsers.suspect import SuspectJsonOutputParser


class SuspectChain:
    def __init__(self, llm):
        self._json_schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "number"},
                "occupation": {"type": "string"},
                "alibi": {"type": "string"},
            },
            "required": ["name", "age", "occupation", "alibi"],
        }

        self._one_shot_example = {
            "killers": [
                {
                    "name": "Gaius",
                    "age": 40,
                    "occupation": "Crazy librarian",
                    "alibi": "Gaius has no alibi. He claims he was in his secret chamber, delving into forbidden texts. No one can vouch for his whereabouts.",
                }
            ],
            "suspects": [
                {
                    "name": "Cassandra",
                    "age": 28,
                    "occupation": "Junior Librarian",
                    "alibi": "Cassandra asserts she was searching for lost texts in the stacks during the homicide. Multiple patrons corroborate her presence near the scene around the estimated time of death.",
                },
                {
                    "name": "Eudoxia",
                    "age": 42,
                    "occupation": "Librarian",
                    "alibi": "On duty cataloging scrolls at the Library of Alexandria during the time of the murder",
                },
            ],
            "themes": [["Library of Alexandria", "340 BC", "crazy librarian"]],
            "victims": [
                {
                    "name": "Archibald Ptolemy",
                    "age": 35,
                    "occupation": "Head Librarian",
                    "murder_weapon": "Ancient scroll with poisoned ink",
                    "death_description": "Found dead in his office surrounded by stacks of books, face contorted in a mixture of fear and surprise, as if he had been reading a particularly gruesome text when struck down.",
                }
            ],
        }

        prompt = PromptTemplate.from_template(
            """
            <s>[INST] <<SYS>>
            
            You are a crime storyteller. Always output your answer in JSON using this scheme: {scheme}.
            Avoid outputting anything else than the JSON answer.
            
            <<SYS>>
            Generate 2 suspects that are not killers of this victim: {victim_example}. Theme of the story is: {theme_example}. Avoid using nicknames.
            suspects:
            [/INST]
            {suspect_examples}</s><s>
            
            [INST]
            Generate 2 suspects that are not killers of this victim: {victim}. Theme of the story is: {theme}. Avoid using nicknames.
            suspects:
            [/INST]
            """
        )

        self._chain = prompt | llm | SuspectJsonOutputParser()

    def create(self, theme, victim):
        return self._chain.invoke(
            {
                "scheme": json.dumps(self._json_schema),
                "theme_example": self._one_shot_example["themes"][0],
                "victim_example": json.dumps(self._one_shot_example["victims"][0]),
                "suspect_examples": json.dumps(self._one_shot_example["suspects"]),
                "theme": theme,
                "victim": json.dumps(victim),
            }
        )
