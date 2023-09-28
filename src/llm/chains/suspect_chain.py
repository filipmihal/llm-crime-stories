from langchain.prompts import PromptTemplate

from llm.output_parsers.suspect import SuspectYamlOutputParser

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

        self._chain = self._suspect_prompt | self._llm | SuspectYamlOutputParser()

    def create(self, theme, victim):
        return self._chain.invoke({"theme": theme, "victim": victim})
