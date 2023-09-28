from llm.marshmallow.schemas.room import RoomSchema
from llm.output_parsers.base_yaml import BaseYamlOutputParser


class RoomYamlOutputParser(BaseYamlOutputParser):
    """
    Parse the output of an LLM call of the Rooms chain to YAML.
    """

    def __init__(self) -> None:
        super().__init__(
            RoomSchema,
            [
                r"- [rR]oom:[\s\S]*",
                r"[rR]oom:[\s\S]*",
                r"- [rR]oom:[\s\S]*\n",
                r"[rR]oom:[\s\S]*\n",
            ],
        )
