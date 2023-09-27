from collections import deque
from langchain.prompts import PromptTemplate

from llm.gen_chains.yaml_output_parser import YamlOutputParser


class RoomsChain:
    def __init__(self, llm, rooms_layout):
        self._llm = llm

        self._rooms_layout = rooms_layout
        self._rows, self._columns = len(rooms_layout), len(rooms_layout[0])

        self._suspect_prompt = PromptTemplate.from_template(
            """
            <s>[INST] <<SYS>>
            You are a crime storyteller. Always output your answer in YAML. No pre-amble.
            <<SYS>>

            The theme of the story is: {{theme}}. Describe a room and here are information about the suspect person that is in there: {{entity}}. [/INST]
            """
        )

        self._victim_prompt = PromptTemplate.from_template(
            """
            <s>[INST] <<SYS>>
            You are a crime storyteller. Always output your answer in YAML. No pre-amble.
            <<SYS>>

            The theme of the story is: {{theme}}. Describe a room where the body was found. The information about the victim: {{entity}}. [/INST]
            """
        )

    def create(self, theme, victim, suspects):
        # generate description for the starting room, assumes square rooms layout
        middle_row, middle_col = self._rows // 2, self._columns // 2
        start_story = self.generate_room(self._victim_prompt, theme, victim)
        start_story.update({"row": middle_row, "col": middle_col})

        # contains final description of rooms
        rooms_data, suspects_positions = [start_story], []

        # generate rest of the rooms
        not_selected_suspects = deque(suspects)
        generated = set([(middle_row, middle_col)])
        q = deque(self._get_neighbours(middle_row, middle_col))
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
        chain = prompt | self._llm | YamlOutputParser()
        return chain.invoke({"theme": theme, "entity": entity})

    def _get_neighbours(self, row, col):
        neighbours = []
        for x, y in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
            if (
                0 <= row + x < self._rows
                and 0 <= col + y < self._columns
                and self._rooms_layout[row + x][col + y]
            ):
                neighbours.append((row + x, col + y))

        return neighbours
