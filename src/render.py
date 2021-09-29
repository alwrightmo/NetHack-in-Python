from colors import dcolor

def render(entities, dungeon, fov_map): # This method has a bunch of unnecessary stuff in it
    boulder_positions = ()
    for entity in entities:
        if entity.name == 'player':
            player = entity
        if entity.name == 'boulder':
            boulder_positions += ((entity.y, entity.x),)

    lines = ''
    for row in range(dungeon.height):
        line = '                                                  ' # 50 Spaces
        for col in range(dungeon.width):               
            if fov_map[row][col] or (player.y == row and player.x == col): # If you should see it
                dungeon.tiles[row][col].display_char = dungeon.tiles[row][col].color_char

                for entity in entities: # Make sure that all entities are drawn on top of the floor
                    if entity.y == row and entity.x == col:
                        dungeon.tiles[row][col].display_char = entity.color_char
                        
                dungeon.tiles[row][col].explored = True # Make all visible space explored
            else:
                if dungeon.tiles[row][col].explored: # If you have seen something, set it's color to grey
                    if ((row, col)) in boulder_positions:
                        dungeon.tiles[row][col].display_char = dcolor.GREY + '0' + dcolor.END
                    elif dungeon.tiles[row][col].char == '.':
                        dungeon.tiles[row][col].display_char = dcolor.GREY + dungeon.tiles[row][col].char + dcolor.END
                    elif dungeon.tiles[row][col].block_sight:
                        dungeon.tiles[row][col].display_char = dungeon.tiles[row][col].char
                    else:
                        pass
                        #dungeon.tiles[row][col].display_char = ' '
            line += ''.join(dungeon.tiles[row][col].display_char)
            
        if row < dungeon.height - 1: # ANSI Escape sequence voodoo magic
            lines += line + '\033[E'
        else:
            lines += line
    print(lines) # Single print statment is always better (right?)
