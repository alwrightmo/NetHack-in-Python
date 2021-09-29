class dcolor: # A default color class for when you don't want to specify
              # a color
    GREY = '\033[38;2;45;45;45m'
    END = '\033[0m'

class color: # Color class to store and handle colors
    def __init__(self, r, g, b, highlight=None):
        self.r = str(r)
        self.g = str(g)
        self.b = str(b)
        self.highlight = highlight

    def color(self):
        if self.highlight:
            return '\033[38;2;' + self.r + ';' + self.g + ';' + self.b + 'm\033[48;2;160;160;160m'
        return '\033[38;2;' + self.r + ';' + self.g + ';' + self.b + 'm'

    def end(self):
        return '\033[0m'
