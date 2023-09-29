import json
from json.decoder import JSONDecodeError
from langchain.schema import BaseOutputParser
from marshmallow import ValidationError
from typing import Optional

from llm.marshmallow.schemas.suspect import SuspectSchema


class SuspectJsonOutputParser(BaseOutputParser):
    """
    Parse the output of an LLM call of the Suspect chain to JSON.
    """

    def parse(self, text: str) -> Optional[SuspectSchema]:
        """
        Parse the output of an LLM call.
        """
        print("suspect" + text)
        try:
            obj = json.loads(text)
            obj = {k.strip():v.strip() for k, v in obj.items()}
            
            return SuspectSchema().load(obj)
        except JSONDecodeError as decode_err:
            print(decode_err)
        except ValidationError as err:
            print(err.messages)
        finally:
            return None
