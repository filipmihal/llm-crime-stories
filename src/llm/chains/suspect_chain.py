from langchain.prompts import PromptTemplate
from langchain.schema import BaseOutputParser
from marshmallow import ValidationError
import re
from typing import Optional
import yaml

from llm.marshmallow.schemas import SuspectSchema

class SuspectYamlOutputParser(BaseOutputParser):
    """Parse the output of an LLM call of the Suspect chain to YAML."""

    def parse(self, text: str) -> Optional[SuspectSchema]:
        """Parse the output of an LLM call."""
        match = (
            re.search(r"- [sS]uspect:[\s\S]*", text)
            or re.search(r"[sS]uspect:[\s\S]*", text)
            or re.search(r"- [sS]uspect:[\s\S]*\n", text)
            or re.search(r"[sS]uspect:[\s\S]*\n", text)
        )
        group = match.group(0)

        if group.startswith("- "):
            group = group[2:]

        if "`" in group:
            group = re.search(r"([^`]+)`", group).group(1).strip()

        obj = yaml.safe_load(group)
        top_level_key = list(obj.keys())[0]
        try:
            return SuspectSchema().load(obj[top_level_key])
        except ValidationError as err:
            print(err.messages)
            return None


class SuspectChain:
    def __init__(self, llm):
        self._llm = llm

        self._suspect_prompt = PromptTemplate.from_template(
            """
            <s>[INST] <<SYS>>
            You are a crime storyteller.
            <<SYS>>

            Given a theme and information about the victim describe a suspect that is not a killer.
            
            An example is below. Note that you must output only created suspect converted to YAML where all properties are on same level.
            
            Example
            suspect: 
              name: "Lucius"
              age: 35
              occupation: "Librarian's Assistant"
              alibi: >
                Lucius claims he was organizing scrolls in the library's main hall at the time of the murder.
                Several witnesses saw him there throughout the evening.
              motive: >
                Lucius had a longstanding feud with Drusilla, who constantly criticized his work and suggested he was not fit for his role.
                He might have wanted to silence her. [/INST]
                                    
            Give the output for the following theme: {theme} and victim information: {victim}
            """
        )

        self._chain = self._suspect_prompt | self._llm | SuspectYamlOutputParser()

    def create(self, theme, victim):
        return self._chain.invoke({"theme": theme, "victim": victim})
