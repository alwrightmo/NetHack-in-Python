class Room: # Room class that handles how each room on the game map should be handled
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def center(self): # Returns the coords at the center of the room (with rounding)
        return int((self.x1 + self.x2) / 2), int((self.y1 + self.y2) / 2)

    def intersect(self, room): # Returns if a room intersects another room
        return (
            self.x1 <= room.x2 and
            self.x2 >= room.x1 and
            self.y1 <= room.y2 and
            self.y2 >= room.y1
            )