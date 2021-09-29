from random import randint as rand
from entities import Entity
from tile import Tile
from room import Room

class Dungeon: # Dungeon class for handling the game map as a whole
    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.tiles = self.initTiles()

    def initTiles(self): # Creates matrix of tile objects
        tiles = list()
        for y in range(self.height): # Have to do it this way so each object is unique
            current_row = []
            for x in range(self.width):
                current_row.append(Tile(True))
            tiles.append(current_row)

        return tiles
        
    def isBlocked(self, x, y): # Checks if the tile is blocked
        if self.tiles[y][x].block:
            return True
        return False

    def createHTunnel(self, x1, x2, y): # Creates a horizontal tunnel between two rooms
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[y][x].block = self.tiles[y][x].block_sight = False

    def createVTunnel(self, y1, y2, x): # Creates a vertical tunnel between two rooms
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[y][x].block = self.tiles[y][x].block_sight = False

    def createRoom(self, room): # Creates the room
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[y][x].block = self.tiles[y][x].block_sight = False
                # Need to do all the stuff below for some weird reason or
                # Top left corner of some rooms is empty during the
                # fillMap call
                self.tiles[y][x].char = '.'
                if self.tiles[y][x].color:
                    self.tiles[y][x].color_char = self.tiles[y][x].color.color() + '.' + self.tiles[y][x].color.end()
                else:
                    self.tiles[y][x].color_char = '.'

    def createMap(self, max_rooms, min_size, max_size, map_width, map_height,
                  player, entities, max_rocks): # Creates all the rooms and tunnels to create the game map
        rooms = []

        for room in range(max_rooms):
            w = rand(min_size, max_size)
            h = rand(min_size, max_size)
            x = rand(1, map_width - w - 1)
            y = rand(1, map_height - h - 1)
            
            new_room = Room(x, y, w, h)

            new_x, new_y = new_room.center()
            
            if (x + w) >= map_width - 1 or (y + h) >= map_height - 1:
                continue
    
            for existing_room in rooms:
                if new_room.intersect(existing_room): # If the room to be added intersects an existing room ignore it
                                                      # If statement is removed produces interesting room shapes
                    break
            else:
                self.createRoom(new_room)

                if len(rooms) == 0: # If room is first room
                    player.x = new_x
                    player.y = new_y
                    self.tiles[new_y][new_x].char = player.char # Place player in the center of the room
                else:
                    prev_x, prev_y = rooms[len(rooms) - 1].center()

                    if rand(0, 1) == 1: # Go left/right then up/down
                        self.createHTunnel(prev_x, new_x, prev_y)
                        self.createVTunnel(prev_y, new_y, new_x)
                    else: # Go up/down then left/right
                        self.createVTunnel(prev_y, new_y, prev_x)
                        self.createHTunnel(prev_x, new_x, new_y)

                rooms.append(new_room)
                self.placeEntities(new_room, entities, max_rocks)
                
        for _ in range(2): # Has to run twice to accurately fill map
            self.fillMap()
                
    def fillMap(self): # Assigns how the walls and floor should look
        for row in range(self.height):
            for col in range(self.width):
                if self.tiles[row][col].block_sight:
                    if ((row + 1 < self.height and col + 1 < self.width) and
                        (row - 1 >= 0 and col - 1 >= 0)):
                        # The if statements below are over complicated
                        # but I believe(hope) they are more efficient
                        # than any other way that this could be done
                        if (set((self.tiles[row + 1][col].char, self.tiles[row - 1][col].char)) & set(('.', '|'))):
                            self.tiles[row][col].char = self.tiles[row][col].color_char = '-'
                        if (set((self.tiles[row][col + 1].char, self.tiles[row][col - 1].char)) & set('.')):
                            self.tiles[row][col].char = self.tiles[row][col].color_char = '|'
                else:
                    self.tiles[row][col].char = self.tiles[row][col].color_char = '.'

    def placeEntities(self, room, entities, max_rocks): # Place random amount of boulders in room
                                                        # TODO: Remove this function in liu of a
                                                        # actual puzzle engine to emulate
                                                        # sokoban, how I'm going to do this is
                                                        # classified
        num_rocks = rand(0, max_rocks)

        for i in range(num_rocks):
            x = rand(room.x1 + 1, room.x2 - 1)
            y = rand(room.y1 + 1, room.y2 - 1)

            if not any ([entity for entity in entities if entity.x == x and entity.y == y]):
                boulder = Entity(x, y, 'boulder', '0')

                entities.append(boulder)
