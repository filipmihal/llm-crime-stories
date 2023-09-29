from langchain.prompts import PromptTemplate

from llm.output_parsers.victim import VictimYamlOutputParser

class VictimChain:
    def __init__(self, llm):
        self._prompt = PromptTemplate.from_template(
            """
            <s>[INST] <<SYS>>
            
            You are a crime storyteller.
            
            <<SYS>>

            Given a theme: "Library of Alexandria, 340 BC, crazy librarian" describe a victim of the story.
            victim:
            [/INST]
            name: "Archibald Ptolemy"
            age: 42
            occupation: "Head librarian"
            murder_weapon: "fragile ancient scroll"
            death_description: >
                Found face down under pile of books with a broken quill pen lodged in his back, surrounded by scattered papyrus rolls.</s><s>
            
            [INST]
            Given a theme: {theme} describe a victim of the story.
            victim:
            [/INST]
            """
        )

        self._chain = self._prompt | llm | VictimYamlOutputParser()

    def create(self, theme):
        return self._chain.invoke({"theme": theme})
