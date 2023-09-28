from langchain.schema import BaseOutputParser
from marshmallow import ValidationError
import re
from typing import Optional
import yaml

from llm.marshmallow.schemas.room import RoomSchema

class RoomYamlOutputParser(BaseOutputParser):
    """Parse the output of an LLM call to YAML."""

    def parse(self, text: str) -> Optional[RoomSchema]:
        """Parse the output of an LLM call."""
        match = (
            re.search(r"- [rR]oom:[\s\S]*", text)
            or re.search(r"[rR]oom:[\s\S]*", text)
            or re.search(r"- [rR]]oom:[\s\S]*\n", text)
            or re.search(r"[rR]oom:[\s\S]*\n", text)
        )
        group = match.group(0)

        if group.startswith('- '):
            group = group[2:]

        if '`' in group:
            group = re.search(r'([^`]+)`', group).group(1).strip()

        obj = yaml.safe_load(group)
        top_level_key = list(obj.keys())[0]
        try:
            return RoomSchema().load(obj[top_level_key])
        except ValidationError as err:
            print(err.messages)
            return None