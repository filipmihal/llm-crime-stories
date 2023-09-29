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
                "motive": {"type": "string"},
            },
            "required": ["name", "age", "occupation", "alibi", "motive"],
        }

        self._one_shot_example = {
            "killers": [
                {
                    "name": "Gaius",
                    "age": 40,
                    "occupation": "Crazy librarian",
                    "alibi": "Gaius has no alibi. He claims he was in his secret chamber, delving into forbidden texts. No one can vouch for his whereabouts.",
                    "motive": "Gaius had become increasingly obsessed with ancient and forbidden knowledge. He believed that by eliminating anyone who questioned him, he could protect the library's secrets.",
                }
            ],
            "suspects": [
                {
                    "name": "Cassandra",
                    "age": 28,
                    "occupation": "Junior Librarian",
                    "motive": "Cassandra felt threatened by Archibald's strict rules and constant criticism of her work. She may have sought revenge through this brutal act.",
                    "alibi": "Cassandra asserts she was searching for lost texts in the stacks during the homicide. Multiple patrons corroborate her presence near the scene around the estimated time of death.",
                }
            ],
            "themes": [
                ["Library of Alexandria", "340 BC", "crazy librarian"]
            ],
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
            
            You are a crime storyteller. Always output answer as JSON using this {scheme}.
            Avoid outputting anything else than the JSON answer.
            
            <<SYS>>

            Given a theme: {theme_example}, an information about the victim: {victim_example}, describe a suspect that is not the killer. There are more suspects. Avoid nicknames.
            suspect:
            [/INST]
            {suspect_example}</s><s>
            
            [INST]
            Given a theme: {theme}, an information about the victim: {victim}, describe a suspect that is not the killer. There are more suspects. Avoid nicknames.
            suspect:
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
                "suspect_example": json.dumps(self._one_shot_example["suspects"][0]),
                "theme": theme,
                "victim": json.dumps(victim),
            }
        )