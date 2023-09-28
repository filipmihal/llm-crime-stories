import json
from langchain.llms import HuggingFacePipeline
from marshmallow import ValidationError

from environment.types import Grid
from llm.llama import Llama
from llm.chains.killer_chain import KillerChain
from llm.chains.rooms_chain import RoomsChain
from llm.chains.suspect_chain import SuspectChain
from llm.chains.victim_chain import VictimChain
from llm.marshmallow.schemas.story import StorySchema


class StoryGenerator:
    def __init__(self, rooms: Grid, llm=None) -> None:
        llama_pipeline = Llama().pipeline if not llm else llm.pipeline
        self._llm = HuggingFacePipeline(pipeline=llama_pipeline)

        self._rooms = rooms

    def create_new_story(
        self, number_of_suspects: int, theme: str, dummy: bool = False
    ) -> StorySchema:
        if dummy:
            with open("./llm-dungeon-adventures/data/dummy.json", "r") as f:
                return json.load(f)

        victim = VictimChain(self._llm).create(theme)
        killer = KillerChain(self._llm).create(theme, victim)

        suspects_chain = SuspectChain(self._llm)
        suspects = [
            suspects_chain.create(theme, victim) for _ in range(number_of_suspects)
        ]

        rooms, suspects_positions = RoomsChain(self._llm, self._rooms).create(
            theme, victim, suspects
        )

        try:
            return StorySchema().load(
                {
                    "theme": theme,
                    "victim": victim,
                    "killer": killer,
                    "suspects": suspects,
                    "rooms": rooms,
                    "suspects_positions": suspects_positions,
                }
            )
        except ValidationError as err:
            print(err.messages)
            return None
