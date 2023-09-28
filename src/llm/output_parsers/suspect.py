from langchain.schema import BaseOutputParser
from marshmallow import ValidationError
import re
from typing import Optional
import yaml

from llm.marshmallow.schemas import SuspectSchema

class SuspectYamlOutputParser(BaseOutputParser):
    """Parse the output of an LLM call of the Suspect chain to YAML."""

    def parse(self, text: str) -> Optional[SuspectSchema]:
        """Parse the output of an LLM call."""
        match = (
            re.search(r"- [sS]uspect:[\s\S]*", text)
            or re.search(r"[sS]uspect:[\s\S]*", text)
            or re.search(r"- [sS]uspect:[\s\S]*\n", text)
            or re.search(r"[sS]uspect:[\s\S]*\n", text)
        )
        group = match.group(0)

        if group.startswith("- "):
            group = group[2:]

        if "`" in group:
            group = re.search(r"([^`]+)`", group).group(1).strip()

        obj = yaml.safe_load(group)
        top_level_key = list(obj.keys())[0]
        try:
            return SuspectSchema().load(obj[top_level_key])
        except ValidationError as err:
            print(err.messages)
            return None