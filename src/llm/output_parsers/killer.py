from llm.marshmallow.schemas.killer import KillerSchema
from llm.output_parsers.base_yaml import BaseYamlOutputParser


class KillerYamlOutputParser(BaseYamlOutputParser):
    """
    Parse the output of an LLM call of the Killer chain to YAML.
    """

    def __init__(self) -> None:
        super().__init__(
            KillerSchema,
            [
                r"- [kK]iller:[\s\S]*",
                r"[kK]iller:[\s\S]*",
                r"- [kK]iller:[\s\S]*\n",
                r"[kK]iller:[\s\S]*\n",
            ],
        )
