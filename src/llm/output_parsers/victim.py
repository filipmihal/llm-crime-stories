from langchain.schema import BaseOutputParser
from marshmallow import ValidationError
import re
from typing import Optional
import yaml

from llm.marshmallow.schemas.victim import VictimSchema

class VictimYamlOutputParser(BaseOutputParser):
    """Parse the output of an LLM call of the Victim chain to YAML."""

    def parse(self, text: str) -> Optional[VictimSchema]:
        """Parse the output of an LLM call."""
        print(text)
        match = (
            re.search(r"- [vV]ictim:[\s\S]*", text)
            or re.search(r"[vV]ictim:[\s\S]*", text)
            or re.search(r"- [vV]ictim:[\s\S]*\n", text)
            or re.search(r"[vV]ictim:[\s\S]*\n", text)
        )
        group = match.group(0)

        if group.startswith('- '):
            group = group[2:]

        if '`' in group:
            group = re.search(r'([^`]+)`', group).group(1).strip()

        obj = yaml.safe_load(group)
        top_level_key = list(obj.keys())[0]
        try:
            return VictimSchema().load(obj[top_level_key])
        except ValidationError as err:
            print(err.messages)
            return None