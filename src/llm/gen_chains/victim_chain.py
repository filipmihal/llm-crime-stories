from langchain.prompts import PromptTemplate

from llm.gen_chains.yaml_output_parser import YamlOutputParser


class VictimChain:
    def __init__(self, llm):
        self._prompt = PromptTemplate.from_template(
            """
            <s>[INST] <<SYS>>
            You are a crime storyteller. Always output your answer in YAML. No pre-amble.
            <<SYS>>

            Create a victim based on the theme: {{theme}}. Give its name, age, occupation, murder weapon and death description.
            Don't use pre-amble and convert it to YAML.
            """
        )

        self._chain = self._prompt | llm | YamlOutputParser()

    def create(self, theme):
        return self._chain.invoke({"theme": theme})
