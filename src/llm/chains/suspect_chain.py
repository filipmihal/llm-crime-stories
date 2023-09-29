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
            "killers": [
                {
                    "name": "Gaius",
                    "age": 40,
                    "occupation": "Crazy librarian",
                    "alibi": "Gaius has no alibi. He claims he was in his secret chamber, delving into forbidden texts. No one can vouch for his whereabouts.",
                    "motive": "Gaius had become increasingly obsessed with ancient and forbidden knowledge. He believed that by eliminating anyone who questioned him, he could protect the library's secrets.",
                },
                {
                    "name": "Daisy Devereaux",
                    "age": 28,
                    "occupation": "Flapper girl at The Hidden Flask",
                    "alibi": "Daisy swears she was out on a date with her beau, Jack, at the time of the murder. She remembers returning to the speakeasy around midnight and finding Elizabeth already deceased. Daisy is known for her flirtatious nature and love of attention, but she denies any involvement in the crime.",
                    "motive": "Daisy is full of hatred towards everything humane. If she could, she would destroy all humanity.",
                },
            ],
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
                {
                    "name": "Eudoxia",
                    "age": 42,
                    "occupation": "Librarian",
                    "alibi": "On duty cataloging scrolls at the Library of Alexandria during the time of the murder",
                    "motive": "Passionate about preserving knowledge, she had no motive to harm anyone at the library.",
                },
                {
                    "name": "Josephine Malone",
                    "age": 34,
                    "occupation": "Bootlegger",
                    "alibi": "She was delivering a shipment of illegal whiskey to the Speakeasy at the time of the murder.",
                    "motive": "Josephine had a thriving bootlegging business and had no reason to harm anyone at the speakeasy; she needed their business for her operations.",
                },
            ],
            "themes": [
                ["Library of Alexandria", "340 BC", "crazy librarian"],
                ["Prohibition Era", "Speakeasy", "Bootlegger"],
            ],
            "victims": [
                {
                    "name": "Archibald Ptolemy",
                    "age": 35,
                    "occupation": "Head Librarian",
                    "murder_weapon": "Ancient scroll with poisoned ink",
                    "death_description": "Found dead in his office surrounded by stacks of books, face contorted in a mixture of fear and surprise, as if he had been reading a particularly gruesome text when struck down.",
                },
                {
                    "name": "Porchikoot Lemanski",
                    "age": 23,
                    "occupation": "Policeman",
                    "murder_weapon": "bottle",
                    "death_description": "His body was found in the middle of a living room of his own appartment. Lots of bottle glass around him. Massive amounts of blood.",
                },
            ],
        }

        self._first_suspect_prompt = PromptTemplate.from_template(
            """
            <s>[INST] <<SYS>>
            
            You are a crime storyteller. Always output answer as JSON using this {scheme}.
            Avoid outputting anything else than the JSON answer.
            
            <<SYS>>

            Given a theme: {theme_example1}, an information about the victim: {victim_example1}, and killer information: {killer_example1}, describe a suspect that is not the killer. Avoid nicknames.
            suspect:
            [/INST]
            {suspect_example1}</s><s>
            
            Given a theme: {theme_example2}, an information about the victim: {victim_example2}, and killer information: {killer_example2}, describe a suspect that is not the killer. Avoid nicknames.
            suspect:
            [/INST]
            {suspect_example2}</s><s>
            
            [INST]
            Given a theme: {theme}, an information about the victim: {victim}, and an information about the killer: {killer}, describe a suspect that is not the killer. Avoid nicknames.
            suspect:
            [/INST]
            """
        )

        self._second_suspect_prompt = PromptTemplate.from_template(
            """
            <s>[INST] <<SYS>>
            
            You are a crime storyteller. Always output answer as JSON using this {scheme}.
            Avoid outputting anything else than the JSON answer.
            
            <<SYS>>

            Given a theme: {theme_example1}, an information about the victim: {victim_example1}, about the killer: {killer_example1} and about the first suspect: {first_suspect_example1} describe the second suspect that is not the killer. Avoid nicknames.
            suspect:
            [/INST]
            {second_suspect_example1}</s><s>
            
            Given a theme: {theme_example2}, an information about the victim: {victim_example2}, about the killer: {killer_example2}, and about the first suspect: {first_suspect_example2} describe the second suspect that is not the killer. Avoid nicknames.
            suspect:
            [/INST]
            {second_suspect_example2}</s><s>

            [INST]
            Given a theme: {theme}, an information about the victim: {victim}, about the killer: {killer}, and about the first suspect: {first_suspect}, describe the second suspect that is not the killer. Avoid nicknames.
            suspect:
            [/INST]
            """
        )

    def create_first_suspect(self, theme, victim, killer):
        chain = self._first_suspect_prompt | self._llm | SuspectJsonOutputParser()

        return chain.invoke(
            {
                "scheme": json.dumps(self._json_schema),
                "theme_example1": self._one_shot_example["themes"][0],
                "theme_example2": self._one_shot_example["themes"][1],
                "victim_example1": json.dumps(self._one_shot_example["victims"][0]),
                "victim_example2": json.dumps(self._one_shot_example["victims"][1]),
                "killer_example1": json.dumps(self._one_shot_example["killers"][0]),
                "killer_example2": json.dumps(self._one_shot_example["killers"][1]),
                "suspect_example1": json.dumps(self._one_shot_example["suspects"][0]),
                "suspect_example2": json.dumps(self._one_shot_example["suspects"][1]),
                "killer": json.dumps(killer),
                "theme": theme,
                "victim": json.dumps(victim),
            }
        )

    def create_second_suspect(self, theme, victim, killer, first_suspect):
        chain = self._second_suspect_prompt | self._llm | SuspectJsonOutputParser()

        return chain.invoke(
            {
                "scheme": json.dumps(self._json_schema),
                "theme_example1": self._one_shot_example["themes"][0],
                "theme_example2": self._one_shot_example["themes"][1],
                "victim_example1": json.dumps(self._one_shot_example["victims"][0]),
                "victim_example2": json.dumps(self._one_shot_example["victims"][1]),
                "killer_example1": json.dumps(self._one_shot_example["killers"][0]),
                "killer_example2": json.dumps(self._one_shot_example["killers"][1]),
                "first_suspect_example1": json.dumps(
                    self._one_shot_example["suspects"][2]
                ),
                "first_suspect_example2": json.dumps(
                    self._one_shot_example["suspects"][3]
                ),
                "second_suspect_example1": json.dumps(
                    self._one_shot_example["suspects"][0]
                ),
                "second_suspect_example2": json.dumps(
                    self._one_shot_example["suspects"][1]
                ),
                "killer": json.dumps(killer),
                "theme": theme,
                "victim": json.dumps(victim),
                "first_suspect": json.dumps(first_suspect),
            }
        )
