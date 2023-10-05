from environment.player_action import PlayerAction
from environment.game_state import GameState
from environment.player.action_result import ActionResult
from typing import List
from random import shuffle

class ActionAccuse(PlayerAction):

    def get_suspects(self, game_state: GameState) -> List[str]:
        suspects = [suspect['name'] for suspect in game_state.suspects.values()]
        shuffle(suspects)
        return suspects
    

    def act(self, game_state: GameState) -> ActionResult:
        suspects = self.get_suspects(game_state)
        killer = game_state.killer['name']
        killer_number = -1
        print("Who do you think is the killer?")
        for i, suspect in enumerate(suspects):
            print(f"{i+1}. {suspect}")
            if suspect == killer:
                killer_number = i+1
        accusation = input("Enter the number: ")
        if accusation == str(killer_number):
            return ActionResult(True,  True)
        else:
            return ActionResult(True, False)