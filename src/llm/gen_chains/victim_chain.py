from langchain.prompts import PromptTemplate

from llm.gen_chains.yaml_output_parser import YamlOutputParser


class VictimChain:
    def __init__(self, llm):
        self._prompt = PromptTemplate.from_template(
            """
            <s>[INST] <<SYS>>
            You are a crime storyteller.
            <<SYS>>

            Given a theme create a victim in a fictional crime story. Victim is described by its name, age, occupation, murder weapon and death description.
            A couple of examples are below. Note: you are to output just YAML of the created victim.
            
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

        self._chain = self._prompt | llm | YamlOutputParser()

    def create(self, theme):
        return self._chain.invoke({"theme": theme})
