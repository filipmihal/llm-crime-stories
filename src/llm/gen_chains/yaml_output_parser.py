import yaml
from langchain.schema import BaseOutputParser


class YamlOutputParser(BaseOutputParser):
    """Parse the output of an LLM call to YAML."""

    def parse(self, text: str):
        """Parse the output of an LLM call."""
        return yaml.load(text)
        
