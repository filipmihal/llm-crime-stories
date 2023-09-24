from environment.types import Location, Position


class Game:
    """
    Game contains the main game logic and the game state.
    """
    
    def __init__(self, current_location: Location):
        self._current_location = current_location
        self._previous_location = None
    
    @property
    def current_location(self) -> Location:
        return self._current_location
    

    def move(self, direction: Position) -> bool:
        if self._current_location.neighbours[direction] is None:
            return False
        
        self._previous_location = self._current_location
        self._current_location = self._current_location.neighbours[direction]
        
        return True
