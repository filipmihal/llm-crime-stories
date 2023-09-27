from langchain.prompts import PromptTemplate
from langchain.schema import BaseOutputParser
import re
import yaml

from llm.gen_chains.yaml_output_parser import YamlOutputParser

class SuspectYamlOutputParser(BaseOutputParser):
    """Parse the output of an LLM call of the Suspect chain to YAML."""

    def parse(self, text: str):
        """Parse the output of an LLM call."""
        match = re.search(r'suspects:[\s\S]*', text)
        yaml_in_text = match.group(0)
        
        return yaml.safe_load(yaml_in_text)

class SuspectChain:
    def __init__(self, llm):
        self._prompt = PromptTemplate.from_template(
            """
            <s>[INST] <<SYS>>
            You are a crime storyteller.
            <<SYS>>

            Given a theme and information about the victim describe 3 suspects, one of whom is the killer. [/INST]
            
            An example is below. Note: you are to output just YAML of the created suspects.
            
            Example 1)
            suspects:
                - name: "Lucius"
                    age: 35
                    occupation: "Librarian's Assistant"
                    alibi: >
                        Lucius claims he was organizing scrolls in the library's main hall at the time of the murder.
                        Several witnesses saw him there throughout the evening.
                    motive: >
                        Lucius had a longstanding feud with Drusilla, who constantly criticized his work and suggested he was not fit for his role.
                        He might have wanted to silence her.
                    is_guilty: false
                - name: "Aelia"
                    age: 30
                    occupation: "Fellow Scholar"
                    alibi: >
                        Aelia says she was conducting research in a separate section of the library. Her colleagues confirm that she was engrossed in her work and didn't leave her area.
                    motive: >
                        Aelia had discovered a hidden manuscript that could have elevated her status in the scholarly community. Drusilla knew about this discovery and might have wanted to steal her thunder.
                    is_guilty: false
                - name: "Gaius"
                    age: 40
                    occupation: "Crazy Librarian"
                    alibi: >
                        Gaius, known as the 'Crazy Librarian,' has no alibi. He claims he was in his secret chamber, delving into forbidden texts. No one can vouch for his whereabouts.
                    motive: >
                        Gaius had become increasingly obsessed with ancient and forbidden knowledge. He believed that by eliminating anyone who questioned him, he could protect the library's secrets.
                    is_guilty: true
                    
            Give the output for the following theme: {theme} and victim information: {victim}
            """
        )

        self._chain = self._prompt | llm | SuspectYamlOutputParser()

    def create(self, theme, victim):
        return self._chain.invoke({"theme": theme, "victim": victim})
