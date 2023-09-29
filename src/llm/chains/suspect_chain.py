import json
from langchain.prompts import PromptTemplate

from llm.output_parsers.suspect import SuspectJsonOutputParser


class SuspectChain:
    def __init__(self, llm):
        self._llm = llm

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

        self._first_suspect_prompt = PromptTemplate.from_template(
            """
            <s>[INST] <<SYS>>
            
            You are a crime storyteller. Always output answer as an array of JSON objects of this scheme: {scheme}.
            Avoid outputting anything else than the array of JSON objects.
            
            <<SYS>>

            Given a theme: {theme_example}, an information about the victim: {victim_example}, and killer information: {killer_example}, describe a suspect that is not the killer. Avoid nicknames.
            suspect:
            [/INST]
            {suspect_example}</s><s>
            
            [INST]
            Given a theme: {theme}, an information about the victim: {victim}, and an information about the killer: {killer}, describe a suspect that is not the killer. Avoid nicknames.
            suspect:
            [/INST]
            """
        )

        self._second_suspect_prompt = PromptTemplate.from_template(
            """
            <s>[INST] <<SYS>>
            
            You are a crime storyteller. Always output answer as an array of JSON objects of this scheme: {scheme}.
            Avoid outputting anything else than the array of JSON objects.
            
            <<SYS>>

            Given a theme: {theme_example}, an information about the victim: {victim_example}, killer information: {killer_example}, and an information about the first suspect: {first_suspect_example}, describe a second suspect that is not the killer. Avoid nicknames.
            suspect:
            [/INST]
            {second_suspect_example}</s><s>
            
            [INST]
            Given a theme: {theme}, an information about the victim: {victim}, killer information: {killer}, and an information about the first suspect: {first_suspect}, describe a second suspect that is not the killer. Avoid nicknames.
            suspect:
            [/INST]
            """
        )

    def create_first_suspect(self, theme, victim, killer):
        chain = self._first_suspect_prompt | self._llm | SuspectJsonOutputParser()

        return chain.invoke(
            {
                "killer": json.dumps(killer),
                "killer_example": json.dumps(self._one_shot_example["killer"]),
                "scheme": json.dumps(self._json_schema),
                "suspect_example": json.dumps(self._one_shot_example["suspects"][0]),
                "theme": theme,
                "theme_example": self._one_shot_example["theme"],
                "victim": json.dumps(victim),
                "victim_example": json.dumps(self._one_shot_example["victim"]),
            }
        )

    def create_second_suspect(self, theme, victim, killer, first_suspect):
        chain = self._second_suspect_prompt | self._llm | SuspectJsonOutputParser()

        return chain.invoke(
            {
                "killer": json.dumps(killer),
                "killer_example": json.dumps(self._one_shot_example["killer"]),
                "scheme": json.dumps(self._json_schema),
                "first_suspect": json.dumps(first_suspect),
                "first_suspect_example": json.dumps(self._one_shot_example["suspects"][0]),
                "second_suspect_example": json.dumps(self._one_shot_example["suspects"][1]),
                "theme": theme,
                "theme_example": self._one_shot_example["theme"],
                "victim": json.dumps(victim),
                "victim_example": json.dumps(self._one_shot_example["victim"]),
            }
        )