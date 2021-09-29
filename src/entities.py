class Entity: # Entity class that handles all entities (player, boulder, etc)
    def __init__(self, x, y, name, char, color=None, block=True):
        self.x = x
        self.y = y
        self.name = name
        self.char = char
        self.block = block
        self.color = color
        if color:
            self.color_char = color.color() + char + color.end()
        else:
            self.color_char = char
        self.tiles_moved = 0

    def move(self, x, y):
        self.x += x
        self.y += y
        self.tiles_moved += 1

def getBlockingEntities(entities, x, y): # Returns if something is blocking an
                                         # entities movement
    for entity in entities:
        if entity.block and entity.x == x and entity.y == y:
            return entity
    return None
