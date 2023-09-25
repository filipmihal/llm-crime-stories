from environment.types import Location, Grid

class GameState:
    def __init__(self, atmosphere: str, current_location: Location, grid: Grid, dungeon_size: int):
        self._atmosphere = atmosphere
        self._current_location = current_location
        self._previous_location = None
        self._grid = grid
        self._dungeon_size = dungeon_size

    @property
    def atmosphere(self) -> str:
        return self._atmosphere

    @property
    def current_location(self) -> Location:
        return self._current_location
    
    @property
    def dungeon_size(self) -> int:
        return self._dungeon_size
    
    @property
    def grid(self) -> Grid:
        return self._grid
    
    @current_location.setter
    def current_location(self, new_location: Location):
        self._previous_location = self._current_location
        self._current_location = new_location
    
