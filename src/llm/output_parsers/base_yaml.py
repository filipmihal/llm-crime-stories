from langchain.schema import BaseOutputParser
from marshmallow import Schema, ValidationError
import re
from typing import List, Optional
import yaml


class BaseYamlOutputParser(BaseOutputParser):
    """
    Represents a parser of the output of an LLM call of a chain to YAML.
    """

    def __init__(self, schema_cls: Schema, patterns: List[str]) -> None:
        self._schema_cls = schema_cls
        self._patterns = patterns

    def parse(self, text: str) -> Optional[Schema]:
        """Parse the output of an LLM call."""
        match = None
        for pattern in self._patterns:
            if match := re.search(pattern, text):
                break
        group = match.group(0)

        if group.startswith("- "):
            group = group[2:]

        if "`" in group:
            group = re.search(r"([^`]+)`", group).group(1).strip()

        obj = yaml.safe_load(group)
        top_level_key = list(obj.keys())[0]
        try:
            return self._schema_cls().load(obj[top_level_key])
        except ValidationError as err:
            print(err.messages)
            return None
