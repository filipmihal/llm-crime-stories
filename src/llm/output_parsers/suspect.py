import json
from langchain.schema import BaseOutputParser
from marshmallow import ValidationError
from typing import Optional

from llm.marshmallow.schemas.suspect import SuspectSchema


class SuspectJSONOutputParser(BaseOutputParser):
    """Parse the output of an LLM call of the Suspect chain to JSON."""

    def parse(self, text: str) -> Optional[SuspectSchema]:
        """Parse the output of an LLM call."""
        obj = json.loads(text)
        return obj
        # try:
        #     return SuspectSchema().load(obj)
        # except ValidationError as err:
        #     print(err.messages)
        #     return None
