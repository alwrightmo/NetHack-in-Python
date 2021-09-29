from subprocess import call
from random import randint as rand
from msvcrt import getch
from entities import Entity, getBlockingEntities
from inp import handlePlayerMove
from render import render
from dungeon import Dungeon
from colors import color
from fov import recomputeFov
from constants import dvals

if __name__ == '__main__':
    '''sokoban_width = rand(60, 100)# 100
    sokoban_height = rand( 30, 50)# 50

    sokoban_max_rooms = (sokoban_width + sokoban_height) // 8 # 15
    sokoban_min_size = sokoban_max_rooms // 3 # 5
    sokoban_max_size = sokoban_max_rooms - sokoban_min_size # 10
    sokoban_max_rocks = sokoban_min_size - 1 '''

    recompute_fov = True
    #radius = 9 # For the fov algorithm

    rgb = ['255', '255', '255']
                    
    player_color = color(rgb[0], rgb[1], rgb[2], True) # Inefficient, feed it one rgb array and sort it out in creation
    
    sokoban = Dungeon(dvals.d_width, dvals.d_height)
    player = Entity(0, 0, 'player', '@', player_color)
    entities = [player]

    sokoban.createMap(dvals.d_max_rooms, dvals.d_min_size, dvals.d_max_size,
                      dvals.d_width, dvals.d_height, player, entities,
                      dvals.d_max_rocks)

    count = 0

    call('color', shell=True) # Strictly windows only to tell cmd to allow ANSI escape sequences
    
    # Game loop (game)
    while True:     
        if recompute_fov:
            fov_map = recomputeFov(player, sokoban, entities, dvals.radius)

        print('\033[F' * (dvals.d_height + 2))
        render(entities, sokoban, fov_map)
        # Remove this eventually for an actual menu display
        # Will be set up very similarly to this with print statments
        print("Player Tiles Moved:", player.tiles_moved,
              "| Map Size:", dvals.d_height, "x", dvals.d_width,
              "| Max Rooms:", dvals.d_max_rooms,
              "| Min/Max Room Size:", dvals.d_min_size, "To", dvals.d_max_size,
              "| Boulders Per Room:", dvals.d_max_rocks,
              "| Player Coords:", player.y, player.x)
        key = ord(getch())
        p_move = handlePlayerMove(key)
        if p_move:
            x, y = p_move
            dest_x = player.x + x
            dest_y = player.y + y
            if not sokoban.isBlocked(dest_x, dest_y): # This is actually kinda nice ngl
                target = getBlockingEntities(entities, dest_x, dest_y)
                if target and target.name == 'boulder':
                    active_targets = [target]
                    dest_x = target.x + x
                    dest_y = target.y + y
                    while target and not sokoban.isBlocked(dest_x, dest_y):
                        # Doing this twice is a necessary evil
                        dest_x = target.x + x
                        dest_y = target.y + y 
                        if not sokoban.isBlocked(dest_x, dest_y):
                            target = getBlockingEntities(entities, dest_x, dest_y)
                            if target:
                                if target in active_targets:
                                    break
                                else:
                                    active_targets.append(target)
                    if not sokoban.isBlocked(dest_x, dest_y):
                        for i in active_targets:
                            i.move(x, y)
                        player.move(x, y)
                        recompute_fov = True
                else:
                    player.move(x, y)
                    recompute_fov = True
