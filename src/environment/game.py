from environment.location import Location


class Game:
    """
    Game contains the main game logic and the game state.
    """
    
    def __init__(self, current_location: Location):
        self.current_location = current_location
        self.previous_location = None

    def move(self, direction: str) -> bool:
        if direction == "north":
            if self.current_location.north is None:
                return False
            self.previous_location = self.current_location
            self.current_location = self.current_location.north
            return True

        if direction == "south":
            if self.current_location.south is None:
                return False
            self.previous_location = self.current_location
            self.current_location = self.current_location.south
            return True

        if direction == "east":
            if self.current_location.east is None:
                return False
            self.previous_location = self.current_location
            self.current_location = self.current_location.east
            return True

        if direction == "west":
            if self.current_location.west is None:
                return False
            self.previous_location = self.current_location
            self.current_location = self.current_location.west
            return True
