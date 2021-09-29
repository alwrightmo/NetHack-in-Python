from entities import getBlockingEntities

mult = [
    [1,  0,  0, -1, -1,  0,  0,  1],
    [0,  1, -1,  0,  0, -1,  1,  0],
    [0,  1,  1,  0,  0, -1, -1,  0],
    [1,  0,  0,  1, -1,  0,  0, -1]
        ]

def initFov(dungeon): # Returns a matrix that is the same size as the game map
                      # full of false values
    fov_map = [[False for _ in range(dungeon.width)] for _ in range(dungeon.height)]

    return fov_map

def getVision(dungeon, fov_map, entities, cx, cy, row, start, end, radius, xx, xy, yx, yy): # Fov algorithm (IDK)
    if start < end: # Recursive fov algorithm
        return
    radius_squared = (radius) * (radius) # Powerful math
    for j in range(row, radius):
        dx, dy = (-j - 1), -j
        blocked = False
        while dx <= 0:
            dx += 1
            x, y = (cx + dx * xx + dy * xy), (cy + dx * yx + dy * yy)
            l_slope, r_slope = ( (dx - .5) / (dy + .5) ), ( (dx + .5) / (dy - .5) )
            if start < r_slope:
                continue
            elif end > l_slope:
                break
            else:
                if dx * dx + dy * dy < radius_squared: # Square should be lit
                    fov_map[y][x] = True
                if blocked: # Square is blocked
                    target = getBlockingEntities(entities, x, y)               
                    if dungeon.tiles[y][x].block or target:
                        new_start = r_slope
                        continue
                    else: #Path opened
                        blocked = False
                        start = new_start
                else:
                    target = getBlockingEntities(entities, x, y)  
                    if (dungeon.tiles[y][x].block or target) and j < radius:
                        blocked = True
                        getVision(dungeon, fov_map, entities, cx, cy, j + 1, start,
                                  l_slope, radius, xx, xy, yx, yy)
                        new_start = r_slope
        if blocked:
            break

    return fov_map
                        
def recomputeFov(player, dungeon, entities, radius):
    fov_map = initFov(dungeon)

    for o in range(8):
        fov_map = getVision(dungeon, fov_map, entities, player.x, player.y,
                        1, 1.0, 0.0, radius, mult[0][o],
                        mult[1][o], mult[2][o], mult[3][o])

    return fov_map
