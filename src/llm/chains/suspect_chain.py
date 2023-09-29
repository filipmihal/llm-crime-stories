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
            "suspect": {
                "name": "Lucius",
                "age": 35,
                "occupation": "Librarian's Assistant",
                "alibi": "Lucius claims he was organizing scrolls in the library's main hall at the time of the murder. Several witnesses saw him there throughout the evening.",
                "motive": "Lucius had a longstanding feud with Drusilla, who constantly criticized his work and suggested he was not fit for his role. He might have wanted to silence her.",
            },
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

            Given a theme: {theme_example} and victim information: {victim_example} describe a suspect that is not a killer. Avoid nicknames.
            suspect:
            [/INST]
            {suspect_example}</s><s>
            
            [INST]
            Given a theme: {theme} and victim information: {victim} describe a suspect that is not a killer. Avoid nicknames.
            suspect:
            [/INST]
            """
        )

        self._chain = prompt | llm | SuspectJsonOutputParser()

    def create(self, theme, victim):
        return self._chain.invoke(
            {
                "scheme": json.dumps(self._json_schema),
                "suspect_example": json.dumps(self._one_shot_example["suspect"]),
                "theme": theme,
                "theme_example": self._one_shot_example["theme"],
                "victim": json.dumps(victim),
                "victim_example": json.dumps(self._one_shot_example["victim"]),
            }
        )
