from environment.player_action import PlayerAction
from environment.player.action_result import ActionResult

class PlayerActionInvalid(PlayerAction):
    def act(self) -> ActionResult:
        print("Invalid instruction")
        return ActionResult(False, False)
