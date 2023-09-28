from llm.marshmallow.schemas.victim import VictimSchema
from llm.output_parsers.base_yaml import BaseYamlOutputParser


class VictimYamlOutputParser(BaseYamlOutputParser):
    """
    Parse the output of an LLM call of the Victim chain to YAML.
    """

    def __init__(self) -> None:
        super().__init__()
        self._validation_schema_cls = VictimSchema
        self._patterns = [
                r"- [vV]ictim:[\s\S]*",
                r"[vV]ictim:[\s\S]*",
                r"- [vV]ictim:[\s\S]*\n",
                r"[vV]ictim:[\s\S]*\n",
            ]
