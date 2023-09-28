from langchain.prompts import PromptTemplate

from llm.output_parsers.victim import VictimYamlOutputParser

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
