from environment.player_action import PlayerAction
from environment.player.action_result import ActionResult

class ActionInvalid(PlayerAction):
    def act(self) -> ActionResult:
        print("Invalid instruction")
        return ActionResult(False, False)
