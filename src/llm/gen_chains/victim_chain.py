from langchain.prompts import PromptTemplate

from llm.gen_chains.yaml_output_parser import YamlOutputParser


class VictimChain:
    def __init__(self, llm):
        self._prompt = PromptTemplate.from_template(
            """
            <s>[INST] <<SYS>>
            You are a crime storyteller. When answering, don't use pre-amble. Just return the result converted to YAML.
            <<SYS>>

            Create a victim based on the theme: {{theme}}. Give its name, age, occupation, murder weapon and death description.
            
            An example of a desired output for a created victim:
            
            - victim:
                name: "Alicia Williams"
                age: 25
                occupation: "nurse"
                murder_weapon: "hunter's knife"
                death_description: "Body lying in blood on the kitchen's floor, stabbed 36 times in the body area"
            """
        )

        self._chain = self._prompt | llm | YamlOutputParser()

    def create(self, theme):
        return self._chain.invoke({"theme": theme})
