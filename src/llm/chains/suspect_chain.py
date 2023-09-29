import json
from langchain.prompts import PromptTemplate

from llm.output_parsers.suspect import SuspectJsonOutputParser


class SuspectChain:
    def __init__(self, llm):
        self._json_schema = {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "age": {"type": "number"},
                    "occupation": {"type": "string"},
                    "alibi": {"type": "string"},
                    "motive": {"type": "string"},
                },
                "required": ["name", "age", "occupation", "alibi", "motive"],
            },
        }

        self._one_shot_example = {
            "killer": {
                "name": "Gaius",
                "age": 40,
                "occupation": "Crazy librarian",
                "alibi": "Gaius has no alibi. He claims he was in his secret chamber, delving into forbidden texts. No one can vouch for his whereabouts.",
                "motive": "Gaius had become increasingly obsessed with ancient and forbidden knowledge. He believed that by eliminating anyone who questioned him, he could protect the library's secrets.",
            },
            "suspects": [
                {
                    "name": "Lucius",
                    "age": 35,
                    "occupation": "Librarian's Assistant",
                    "alibi": "Lucius claims he was organizing scrolls in the library's main hall at the time of the murder. Several witnesses saw him there throughout the evening.",
                    "motive": "Lucius had a longstanding feud with Drusilla, who constantly criticized his work and suggested he was not fit for his role. He might have wanted to silence her.",
                },
                {
                    "name": "Cassandra",
                    "age": 28,
                    "occupation": "Junior Librarian",
                    "motive": "Cassandra felt threatened by Archibald's strict rules and constant criticism of her work. She may have sought revenge through this brutal act.",
                    "alibi": "Cassandra asserts she was searching for lost texts in the stacks during the homicide. Multiple patrons corroborate her presence near the scene around the estimated time of death.",
                },
            ],
            "theme": "Library of Alexandria, 340 BC, crazy librarian",
            "victim": {
                "name": "Archibald Ptolemy",
                "age": 35,
                "occupation": "Head Librarian",
                "murder_weapon": "Ancient scroll with poisoned ink",
                "death_description": "Found dead in his office surrounded by stacks of books, face contorted in a mixture of fear and surprise, as if he had been reading a particularly gruesome text when struck down.",
            },
        }

        prompt = PromptTemplate.from_template(
            """
            <s>[INST] <<SYS>>
            
            You are a crime storyteller. Always output answer as JSON using this {scheme}.
            Avoid outputting anything else than the JSON answer.
            
            <<SYS>>

            Given a theme: {theme_example}, victim information: {victim_example} and killer information: {killer_example}, describe 2 suspects that are not the killer. Avoid nicknames.
            suspects:
            [/INST]
            {suspects_example}</s><s>
            
            [INST]
            Given a theme: {theme}, victim information: {victim} and killer information: {killer}, describe 2 suspect that are not the killer. Avoid nicknames.
            suspects:
            [/INST]
            """
        )

        self._chain = prompt | llm | SuspectJsonOutputParser()

    def create(self, theme, victim, killer):
        return self._chain.invoke(
            {
                "killer": json.dumps(killer),
                "killer_example": json.dumps(self._one_shot_example["killer"]),
                "scheme": json.dumps(self._json_schema),
                "suspects_example": json.dumps(self._one_shot_example["suspects"]),
                "theme": theme,
                "theme_example": self._one_shot_example["theme"],
                "victim": json.dumps(victim),
                "victim_example": json.dumps(self._one_shot_example["victim"]),
            }
        )
