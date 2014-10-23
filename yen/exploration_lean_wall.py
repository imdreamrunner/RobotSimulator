WIDTH = 20
HEIGHT = 15

CHALLENGE_EXPLORE_REACH_GOAL = 0
CHALLENGE_EXPLORE_REACH_START = 1
CHALLENGE_RUN_REACH_GOAL = 2
CHALLENGE_RUN_FINISH = 3

STATE_PREFER_GO = 0
STATE_PREFER_RIGHT = 1

DX = [-1, 0, 1, 0]
DY = [0, 1, 0, -1]

state = STATE_PREFER_GO


def is_outside(x, y):
    return x < 0 or x >= HEIGHT or y < 0 or y >= WIDTH


def is_obstacle(known_world, x, y):
    if is_outside(x, y):
        return True
    return known_world[x][y] == 2


def is_free(known_world, x, y):
    if is_outside(x, y):
        return False
    return known_world[x][y] == 1


def is_standable(known_world, x, y):
    for i in range(3):
        for j in range(3):
            if not is_free(known_world, x+i-1, y+j-1):
                return False
    return True


def can_not_standable(known_world, x, y):
    for i in range(3):
        for j in range(3):
            if is_obstacle(known_world, x+i-1, y+j-1):
                return True
    return False


def explore(known_world, x, y, d, goalX, goalY, challenge):
    global state

    if challenge == CHALLENGE_EXPLORE_REACH_GOAL:
        if d == 2:
            state = STATE_PREFER_GO

    if state == STATE_PREFER_GO:
        if is_standable(known_world, x + DX[d], y + DY[d]):
            state = STATE_PREFER_RIGHT
            return 0
        else:
            state = STATE_PREFER_GO
            return 3
    else:
        # state = STATE_PREFER_RIGHT
        if can_not_standable(known_world, x + DX[right(d)], y + DY[right(d)]):
            if is_standable(known_world, x + DX[d], y + DY[d]):
                state = STATE_PREFER_RIGHT
                return 0
            else:
                state = STATE_PREFER_GO
                return 3
        else:
            state = STATE_PREFER_GO
            return 2


def left(d):
    return (d+3) % 4


def right(d):
    return (d+1) % 4


