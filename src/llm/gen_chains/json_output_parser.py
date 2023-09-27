import json
from langchain.schema import BaseOutputParser


class JsonOutputParser(BaseOutputParser):
    """Parse the output of an LLM call to a JSON."""

    def parse(self, text: str):
        """Parse the output of an LLM call."""
        return text
        
