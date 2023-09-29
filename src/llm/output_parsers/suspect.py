import json
from json.decoder import JSONDecodeError
from langchain.schema import BaseOutputParser
from marshmallow import ValidationError
from typing import List, Optional

from llm.marshmallow.schemas.suspect import SuspectSchema


class SuspectJsonOutputParser(BaseOutputParser):
    """
    Parse the output of an LLM call of the Suspect chain to JSON.
    """

    def parse(self, text: str) -> Optional[List[SuspectSchema]]:
        """
        Parse the output of an LLM call.
        """
        print("suspects" + text)
        try:
            obj = json.loads(text)
            obj = [{k.strip():v.strip() for k, v in o.items()} for o in obj]
            
            return [SuspectSchema().load(o) for o in obj]
        except JSONDecodeError as decode_err:
            print(decode_err)
        except ValidationError as err:
            print(err.messages)
        finally:
            return None
