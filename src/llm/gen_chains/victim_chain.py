from langchain.prompts import PromptTemplate
from langchain.schema import BaseOutputParser
import re
import yaml


class VictimYamlOutputParser(BaseOutputParser):
    """Parse the output of an LLM call of the Victim chain to YAML."""

    def parse(self, text: str):
        """Parse the output of an LLM call."""
        # print(text)
        match = (
            re.search(r"- [vV]ictim:[\s\S]*", text)
            or re.search(r"[vV]ictim:[\s\S]*", text)
            or re.search(r"- [vV]ictim:[\s\S]*\n", text)
            or re.search(r"[vV]ictim:[\s\S]*\n", text)
        )
        group = match.group(0)

        if group.startswith('- '):
            group = group[2:]

        if '`' in group:
            group = re.search(r'([^`]+)`', group).group(1).strip()
        
        return yaml.safe_load(group)


class VictimChain:
    def __init__(self, llm):
        self._prompt = PromptTemplate.from_template(
            """
            <s>[INST] <<SYS>>
            You are a crime storyteller.
            <<SYS>>

            Given a theme create a victim in a fictional crime story. Victim is described by its name, age, occupation, murder weapon and death description.
            An example is below. Note that output only created victim converted to YAML where all properties are on the same level.
            
            Example
            Question: Give the output for the following theme: hospital, hunting.
            Answer: 
            victim:
              name: "Alicia Williams"
              age: 25
              occupation: "nurse"
              murder_weapon: "hunter's knife"
              death_description: "Body lying in blood on the kitchen's floor, stabbed 36 times in the body area" [/INST]
            
            Give the output for the following theme: {theme}
            """
        )

        self._chain = self._prompt | llm | VictimYamlOutputParser()

    def create(self, theme):
        return self._chain.invoke({"theme": theme})
