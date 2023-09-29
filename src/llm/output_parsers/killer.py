import json
from langchain.schema import BaseOutputParser
from marshmallow import ValidationError
import re

from llm.marshmallow.schemas.killer import KillerSchema

class KillerJsonOutputParser(BaseOutputParser):
    """Parse the output of an LLM call of the Killer chain to YAML."""

    def parse(self, text: str):
        """Parse the output of an LLM call."""
        obj = json.loads(text)
        return obj
        # try:
        #     return KillerSchema().load(obj)
        # except ValidationError as err:
        #     print(err.messages)
        #     return None