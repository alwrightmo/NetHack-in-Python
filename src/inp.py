def handlePlayerMove(key): # Handles player input and returns the way a player should move if at all
    if key in [119, 56]: # Up
        return 0, -1
    elif key == 55: # Up Left
        return -1, -1
    elif key in [97, 52]: # Left
        return -1, 0
    elif key == 49: # Down Left
        return -1, 1
    elif key in [115, 50]: # Down
        return 0, 1
    elif key == 51: # Down Right
        return 1, 1
    elif key in [100, 54]: # Right
        return 1, 0
    elif key == 57: # Up Right
        return 1, -1
    else: # Not a valid input
        return None
