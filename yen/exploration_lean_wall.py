from constants import *
from queue import Task

STATE_PREFER_GO = 0
STATE_PREFER_RIGHT = 1
state = STATE_PREFER_GO


def explore_lean_wall(arena, robot, goalX, goalY, visited, challenge):
    global state

    if challenge == CHALLENGE_EXPLORE_REACH_GOAL:
        if robot.d == 2:
            state = STATE_PREFER_GO

    if challenge == CHALLENGE_EXPLORE_REACH_START:
        if robot.d == 0:
            state = STATE_PREFER_GO

    if state == STATE_PREFER_GO:
        if arena.is_standable(robot.x + DX[robot.d], robot.y + DY[robot.d]):
            state = STATE_PREFER_RIGHT
            return [Task(GO_STRAIGHT, 1)]
        else:
            state = STATE_PREFER_GO
            return [Task(TURN_LEFT, 1)]
    else:
        # state = STATE_PREFER_RIGHT
        if arena.can_not_standable(robot.x + DX[right(robot.d)], robot.y + DY[right(robot.d)]):
            if arena.is_standable(robot.x + DX[robot.d], robot.y + DY[robot.d]):
                state = STATE_PREFER_RIGHT
                return [Task(GO_STRAIGHT, 1)]
            else:
                state = STATE_PREFER_GO
                return [Task(TURN_LEFT, 1)]
        else:
            state = STATE_PREFER_GO
            return [Task(TURN_RIGHT, 1)]



