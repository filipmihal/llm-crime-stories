from langchain.prompts import PromptTemplate
from langchain.schema import BaseOutputParser
import re
import yaml


class VictimYamlOutputParser(BaseOutputParser):
    """Parse the output of an LLM call of the Victim chain to YAML."""

    def parse(self, text: str):
        """Parse the output of an LLM call."""
        match = (
            re.search(r"- victim:[\s\S]*", text)
            or re.search(r"victim:[\s\S]*", text)
            or re.search(r"- victim:[\s\S]*\n", text)
            or re.search(r"victim:[\s\S]*\n", text)
        )
        yaml_in_text = match.group(0)

        if not yaml_in_text.startswith("-"):
            yaml_in_text = "- " + yaml_in_text

        return yaml.safe_load(yaml_in_text)


class VictimChain:
    def __init__(self, llm):
        self._prompt = PromptTemplate.from_template(
            """
            <s>[INST] <<SYS>>
            You are a crime storyteller.
            <<SYS>>

            Given a theme create a victim in a fictional crime story. Victim is described by its name, age, occupation, murder weapon and death description.
            A couple of examples are below. Note: do not output anything else other than just the YAML of a created victim.
            
            Example 1)
            - victim:
                name: "Alicia Williams"
                age: 25
                occupation: "nurse"
                murder_weapon: "hunter's knife"
                death_description: "Body lying in blood on the kitchen's floor, stabbed 36 times in the body area"
                
            Example 2)
            - victim:
                name: "Bradley Johnson"
                age: 42
                occupation: "lawyer"
                murder_weapon: "handgun"
                death_description: "Body found in the garage with one bullet wound to the chest, signs of strangulation"
            
            Give the output for the following theme:
            {theme}
            """
        )

        self._chain = self._prompt | llm | VictimYamlOutputParser()

    def create(self, theme):
        return self._chain.invoke({"theme": theme})
