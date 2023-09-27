from collections import deque
import json
from langchain.prompts import PromptTemplate

from llm.gen_chains.json_output_parser import JsonOutputParser


class RoomsChain:
    def __init__(self, llm, rooms_layout):
        self._llm = llm

        self._rooms_layout = rooms_layout
        self._rows, self._columns = len(rooms_layout), len(rooms_layout[0])

        self._json_schema = json.dump(
            {
                "$schema": "http://json-schema.org/draft-07/schema#",
                "title": "Generated schema for Root",
                "type": "object",
                "properties": {
                    "room_name": {"type": "string"},
                    "description": {"type": "string"},
                },
                "required": ["room_name", "description"],
            }
        )

        self._suspect_prompt = PromptTemplate.from_template(
            """
            You are a crime storyteller. The theme of the story is: {{theme}}.
            Describe a room and this person is in there: {{entity}}.
            Return the response in the following json schema {{schema}}.
        """
        )

        self._victim_prompt = PromptTemplate.from_template(
            """
            You are a crime storyteller. The theme of the story is: {{theme}}.
            Describe a room where the body was found. The information about the victim: {{entity}}.
            Return the response in the following json schema {{schema}}.
        """
        )

    def create(self, theme, victim, suspects):
        # firstly, generate description for the starting room, assumes square rooms layout
        middle_row, middle_col = self._rows // 2 + 1, self._columns // 2 + 1
        start_story = self.generate_room(self._victim_prompt, theme, victim)
        start_story.update({"row": middle_row, "col": middle_col})

        # contains final description of rooms
        rooms_data, suspects_positions = [start_story], []

        # generate rest of the rooms
        not_selected_suspects = deque(suspects)
        generated = set([(middle_row, middle_col)])
        q = deque(list(self._get_neighbours(middle_row, middle_col)))
        while q:
            current_room = q.pop()
            if current_room in generated:
                continue

            row, col = current_room

            current_room_story = self.generate_room(
                self._suspect_prompt, theme, not_selected_suspects.popleft()
            )
            current_room_story.update({"row": row, "j": col})
            rooms_data.append(current_room_story)

            generated.add((row, col))
            q.extend(self._get_neighbours(row, col))
            suspects_positions.append((row, col))

        return rooms_data, suspects_positions

    def generate_room(self, prompt, theme, entity):
        chain = prompt | self._llm | JsonOutputParser()
        return chain.invoke(
            {"theme": theme, "entity": entity, "schema": self._json_schema}
        )

    def _get_neighbours(self, row, col):
        neighbours = []
        for x, y in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
            if (
                0 <= row + x < self.rows
                and 0 <= col + y < self._columns
                and self._rooms_layout[row + x][col + y]
            ):
                neighbours.append((row + x, col + y))
