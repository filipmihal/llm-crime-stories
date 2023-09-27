from langchain.prompts import PromptTemplate
from langchain.schema import BaseOutputParser
import re
import yaml


class SuspectYamlOutputParser(BaseOutputParser):
    """Parse the output of an LLM call of the Suspect chain to YAML."""

    def parse(self, text: str):
        """Parse the output of an LLM call."""
        match = (
            re.search(r"- [sS]uspect:[\s\S]*", text)
            or re.search(r"[sS]uspect:[\s\S]*", text)
            or re.search(r"- [sS]uspect:[\s\S]*\n", text)
            or re.search(r"[sS]uspect:[\s\S]*\n", text)
        )
        group = match.group(0)

        if group.startswith('- '):
            group = group[2:]

        if "`" in group:
            group = re.search(r"([^`]+)`", group).group(1).strip()

        return yaml.safe_load(group)


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

        return yaml.safe_load(group)


class SuspectChain:
    def __init__(self, llm):
        self._llm = llm

        self._suspect_prompt = PromptTemplate.from_template(
            """
            <s>[INST] <<SYS>>
            You are a crime storyteller.
            <<SYS>>

            Given a theme and information about the victim describe a suspect that is not a killer.
            
            An example is below. Note that you must output only created suspect converted to YAML where all properties are on same level.
            
            Example
            suspect: 
              name: "Lucius"
              age: 35
              occupation: "Librarian's Assistant"
              alibi: >
                Lucius claims he was organizing scrolls in the library's main hall at the time of the murder.
                Several witnesses saw him there throughout the evening.
              motive: >
                Lucius had a longstanding feud with Drusilla, who constantly criticized his work and suggested he was not fit for his role.
                He might have wanted to silence her. [/INST]
                                    
            Give the output for the following theme: {theme} and victim information: {victim}
            """
        )

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

    def create(self, number_of_suspects, theme, victim):
        suspects = []

        self._killer_chain = self._killer_prompt | self._llm | KillerYamlOutputParser()
        suspects.append(self._killer_chain.invoke({"theme": theme, "victim": victim}))

        self._suspect_chain = self._suspect_prompt | self._llm | SuspectYamlOutputParser()
        for _ in range(number_of_suspects):
          suspects.append(self._suspect_chain.invoke({"theme": theme, "victim": victim}))

        return suspects
