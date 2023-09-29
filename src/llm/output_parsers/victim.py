import json
from langchain.schema import BaseOutputParser
from marshmallow import ValidationError
import re
from typing import Optional
import yaml

from llm.marshmallow.schemas.victim import VictimSchema

class VictimJsonOutputParser(BaseOutputParser):
    """Parse the output of an LLM call of the Victim chain to YAML."""

    def parse(self, text: str) -> Optional[VictimSchema]:
        """Parse the output of an LLM call."""
        obj = json.loads(text)
        return obj        
        # try:
        #     return VictimSchema().load(obj[top_level_key])
        # except ValidationError as err:
        #     print(err.messages)
        #     return None