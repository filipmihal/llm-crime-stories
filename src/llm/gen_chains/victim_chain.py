from langchain.prompts import PromptTemplate

from llm.gen_chains.yaml_output_parser import YamlOutputParser


class VictimChain:
    def __init__(self, llm):
        self._prompt = PromptTemplate.from_template(
            """
            <s>[INST] <<SYS>>
            You are a crime storyteller. Always output your answer in YAML. No pre-amble.
            <<SYS>>

            The theme of the story is: {{theme}}. Describe a victim's name, age, occupation, murder weapon and death description.
            Dont forget '-' before victim in YAML to denote an object.
            
            For example:
            ```
            - victim:
                name: "Alicia Williams"
                age: 25
                occupation: "nurse"
                murder_weapon: "hunter's knife"
                death_description: "Body lying in blood on the kitchen's floor, stabbed 36 times in the body area"    
            ```
            """
        )

        self._chain = self._prompt | llm | YamlOutputParser()

    def create(self, theme):
        return self._chain.invoke({"theme": theme})
