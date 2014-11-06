DX = [-1, 0, 1, 0]
DY = [0, 1, 0, -1]
SX = [0, 1, 0, -1]
SY = [1, 0, -1, 0]

WIDTH = 20
HEIGHT = 15

CHALLENGE_EXPLORE_REACH_GOAL = 0
CHALLENGE_EXPLORE_REACH_GOAL_1 = 1
CHALLENGE_EXPLORE_REACH_START = 2
CHALLENGE_RUN_REACH_GOAL = 3
CHALLENGE_RUN_FINISH = 4

NO_ACTION = -1
GO_STRAIGHT = 0
TURN_RIGHT = 1
TURN_LEFT = 3
KELLY = 4
SEND_MAP = 5

ACTION_LIST = [GO_STRAIGHT, TURN_RIGHT, TURN_LEFT]

DISPLAY_MAP = False


def get_grid(x, y, d, dd):
    newx = x + DX[d] * dd
    newy = y + DY[d] * dd
    return newx, newy


def left(d):
    return (d+3) % 4


def right(d):
    return (d+1) % 4