from langchain.schema import BaseOutputParser
import re
import yaml

class YamlOutputParser(BaseOutputParser):
    """Parse the output of an LLM call to YAML."""

    def parse(self, text: str):
        """Parse the output of an LLM call."""
        match = re.search(r'- victim:[\s\S]*', text) or re.search(r'victim:[\s\S]*', text)
        yaml_in_text = match.group(0)
        
        if not yaml_in_text.startswith('-'):
            yaml_in_text = '- ' + yaml_in_text

        return yaml.safe_load(yaml_in_text)
        
