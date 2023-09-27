from langchain.prompts import PromptTemplate

from llm.gen_chains.yaml_output_parser import YamlOutputParser


class SuspectChain:
    def __init__(self, llm):
        self._prompt = PromptTemplate.from_template(
            """
            <s>[INST] <<SYS>>
            You are a crime storyteller. Always output your answer in YAML. No pre-amble.
            <<SYS>>

            The theme of the story is: {{theme}}. Describe 3 suspects, one of whom is the killer. Information about the victim: {{victim}}. [/INST]
            """
        )

        self._chain = self._prompt | llm | YamlOutputParser()

    def create(self, theme, victim):
        return self._chain.invoke({"theme": theme, "victim": victim})
