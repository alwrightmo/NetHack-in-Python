class Tile: # Tile class that handles how each area on the game map should be handled
    def __init__(self, block, char=' ', color=None, block_sight=None):
        self.block = block
        self.char = char
        self.color = color
        if color: # If the tile is given a color, set its color character to that
            self.color_char = color.color() + char + color.end()
        else:
            self.color_char = char
        self.display_char = self.color_char
        self.block_sight = block if block_sight is None else block_sight # If block_sight has a value,
                                                                         # set block_sight to said value
                                                                         # else set it to block
        self.explored = False