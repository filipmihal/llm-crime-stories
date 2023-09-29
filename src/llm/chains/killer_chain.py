import json
from langchain.prompts import PromptTemplate

from llm.output_parsers.killer import KillerJsonOutputParser


class KillerChain:
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
            "killer": {
                "name": "Gaius",
                "age": 40,
                "occupation": "Crazy librarian",
                "alibi": "Gaius has no alibi. He claims he was in his secret chamber, delving into forbidden texts. No one can vouch for his whereabouts.",
                "motive": "Gaius had become increasingly obsessed with ancient and forbidden knowledge. He believed that by eliminating anyone who questioned him, he could protect the library's secrets.",
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

            Given a theme: {theme_example} and victim information: {victim_example}, describe a killer. Avoid nicknames.
            killer:
            [/INST]
            {killer_example}</s><s>
            
            [INST]
            Given a theme: {theme} and victim information: {victim}, describe a killer. Avoid nicknames.
            killer:
            [/INST]
            """
        )

        self._chain = prompt | llm | KillerJsonOutputParser()

    def create(self, theme, victim):
        return self._chain.invoke(
            {
                "killer_example": json.dumps(self._one_shot_example["killer"]),
                "scheme": json.dumps(self._json_schema),
                "theme": theme,
                "theme_example": self._one_shot_example["theme"],
                "victim": json.dumps(victim),
                "victim_example": json.dumps(self._one_shot_example["victim"]),
            }
        )
