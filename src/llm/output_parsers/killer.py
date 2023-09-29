import json
from json.decoder import JSONDecodeError
from langchain.schema import BaseOutputParser
from marshmallow import ValidationError
from typing import Optional

from llm.marshmallow.schemas.killer import KillerSchema


class KillerJsonOutputParser(BaseOutputParser):
    """
    Parse the output of an LLM call of the Killer chain to JSON.
    """

    def parse(self, text: str) -> Optional[KillerSchema]:
        """
        Parse the output of an LLM call.
        """
        try:
            return KillerSchema().load(json.loads(text))
        except JSONDecodeError as decode_err:
            print(decode_err)
        except ValidationError as err:
            print(err.messages)
        finally:
            return None
