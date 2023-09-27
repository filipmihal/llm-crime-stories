from langchain.schema import BaseOutputParser
import re
import yaml

class YamlOutputParser(BaseOutputParser):
    """Parse the output of an LLM call to YAML."""

    def parse(self, text: str):
        """Parse the output of an LLM call."""
        print(text)
        yaml_in_text = re.search(r'- victim:[\s\S]*', text).group(0)
        return yaml.safe_load(yaml_in_text)
        
