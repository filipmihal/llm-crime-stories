"""
Location class is a unit of space in the dungeon game. It serves as a descriptor for the world.
"""


class Location:
    def __init__(self):
        self.description = None
        self.south = None
        self.north = None
        self.east = None
        self.west = None

    @staticmethod
    def connect(location1, location2, direction):
        if direction == "north":
            location1.north = location2
            location2.south = location1
        elif direction == "south":
            location1.south = location2
            location2.north = location1
        elif direction == "east":
            location1.east = location2
            location2.west = location1
        elif direction == "west":
            location1.west = location2
            location2.east = location1
        else:
            raise ValueError("Invalid direction")
