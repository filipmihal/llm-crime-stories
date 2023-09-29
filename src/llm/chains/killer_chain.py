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

            Given a theme: "Library of Alexandria, 340 BC, crazy librarian" and victim information: "{'name': 'Archibald Ptolemy', 'age': 35, 'occupation': 'Head Librarian', 'murder_weapon': 'Ancient scroll with poisoned ink', 'death_description': 'Found dead in his office surrounded by stacks of books, face contorted in a mixture of fear and surprise, as if he had been reading a particularly gruesome text when struck down.'}" describe a killer.
            killer:
            [/INST]
            name: "Gaius"
            age: 40
            occupation: "Crazy Librarian"
            alibi: >
              Gaius, known as the 'Crazy Librarian,' has no alibi. He claims he was in his secret chamber, delving into forbidden texts.
              No one can vouch for his whereabouts.
            motive: >
              Gaius had become increasingly obsessed with ancient and forbidden knowledge.
              He believed that by eliminating anyone who questioned him, he could protect the library's secrets.</s><s>
            
            [INST]
            Given a theme: {theme} and victim information: {victim} describe a killer.
            killer:
            [/INST]
            """
        )
        
        self._chain = self._killer_prompt | self._llm | KillerYamlOutputParser()
        
    def create(self, theme, victim):
        return self._chain.invoke({"theme": theme, "victim": victim})