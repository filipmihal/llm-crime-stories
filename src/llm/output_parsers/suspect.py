from llm.marshmallow.schemas.suspect import SuspectSchema
from llm.output_parsers.base_yaml import BaseYamlOutputParser


class SuspectYamlOutputParser(BaseYamlOutputParser):
    """
    Parse the output of an LLM call of the Suspect chain to YAML.
    """

    def __init__(self) -> None:
        super().__init__(
            SuspectSchema,
            [
                r"- [sS]uspect:[\s\S]*",
                r"[sS]uspect:[\s\S]*",
                r"- [sS]uspect:[\s\S]*\n",
                r"[sS]uspect:[\s\S]*\n",
            ],
        )
