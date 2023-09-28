from langchain.prompts import PromptTemplate

from llm.output_parsers.killer import KillerYamlOutputParser

class KillerChain:
    def __init__(self, llm):
        self._llm = llm

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
        
        self._chain = self._killer_prompt | self._llm | KillerYamlOutputParser()
        
    def create(self, theme, victim):
        return self._chain.invoke({"theme": theme, "victim": victim})