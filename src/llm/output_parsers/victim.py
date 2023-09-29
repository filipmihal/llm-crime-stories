import json
from json.decoder import JSONDecodeError
from langchain.schema import BaseOutputParser
from marshmallow import ValidationError
from typing import Optional

from llm.marshmallow.schemas.victim import VictimSchema


class VictimJsonOutputParser(BaseOutputParser):
    """
    Parse the output of an LLM call of the Victim chain to JSON.
    """

    def parse(self, text: str) -> Optional[VictimSchema]:
        """
        Parse the output of an LLM call.
        """
        try:
            obj = re.find(r'\{[^{}]*\}', text)
            obj = json.loads(obj)
            obj = {k.strip():v for k, v in obj.items()}
            
            return VictimSchema().load(obj)
        except JSONDecodeError as decode_err:
            print(decode_err)
            return None
        except ValidationError as err:
            print(err.messages)
            return None
