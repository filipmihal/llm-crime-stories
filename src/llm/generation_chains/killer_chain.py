from langchain.prompts import PromptTemplate
from langchain.schema import BaseOutputParser
from marshmallow import ValidationError
import re
import yaml

from llm.marshmallow.schemas import KillerSchema

class KillerYamlOutputParser(BaseOutputParser):
    """Parse the output of an LLM call of the Killer chain to YAML."""

    def parse(self, text: str):
        """Parse the output of an LLM call."""
        match = (
            re.search(r"- [kK]iller:[\s\S]*", text)
            or re.search(r"[kK]iller:[\s\S]*", text)
            or re.search(r"- [kK]iller:[\s\S]*\n", text)
            or re.search(r"[kK]iller:[\s\S]*\n", text)
        )
        group = match.group(0)

        if group.startswith('- '):
            group = group[2:]

        if "`" in group:
            group = re.search(r"([^`]+)`", group).group(1).strip()

        obj = yaml.safe_load(group)
        try:
            return KillerSchema.load(obj)
        except ValidationError as err:
            print(err.messages)
            return None

class KillerChain:
    def __init__(self, llm):
        self._llm = llm

        self._killer_prompt = PromptTemplate.from_template(
            """
            <s>[INST] <<SYS>>
            You are a crime storyteller.
            <<SYS>>

            Given a theme and information about the victim describe a killer.
            
            An example is below. Note that you must output only created killer converted to YAML where all properties are on same level.
            
            Example
            killer: 
              name: "Gaius"
              age: 40
              occupation: "Crazy Librarian"
              alibi: >
                Gaius, known as the 'Crazy Librarian,' has no alibi. He claims he was in his secret chamber, delving into forbidden texts.
                No one can vouch for his whereabouts.
              motive: >
                Gaius had become increasingly obsessed with ancient and forbidden knowledge.
                He believed that by eliminating anyone who questioned him, he could protect the library's secrets. [/INST]
                                    
            Give the output for the following theme: {theme} and victim information: {victim}
            """
        )
        
        self._chain = self._killer_prompt | self._llm | KillerYamlOutputParser()
        
    def create(self, theme, victim):
        return self._chain.invoke({"theme": theme, "victim": victim})