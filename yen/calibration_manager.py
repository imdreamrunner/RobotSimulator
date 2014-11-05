from constants import *


def can_calibrate_front(arena, robot):
    """
    Return true if there are 3 obstacles at front
    """
    cell1_x, cell1_y = robot.x + SX[robot.d] + 2*DX[robot.d], robot.y + SY[robot.d] + 2*DY[robot.d]
    cell2_x, cell2_y = robot.x - SX[robot.d] + 2*DX[robot.d], robot.y - SY[robot.d] + 2*DY[robot.d]
    cell3_x, cell3_y = robot.x + 2*DX[robot.d], robot.y + 2*DY[robot.d]
    return arena.is_obstacle(cell1_x, cell1_y) and arena.is_obstacle(cell2_x, cell2_y) and arena.is_obstacle(cell3_x, cell3_y)


def can_calibrate_right(arena, robot):
    """
    Return true if the robot can calibrate front after turn right
    """
    cell1_x, cell1_y = robot.x + 2*SX[robot.d] + DX[robot.d], robot.y + 2*SY[robot.d] + DY[robot.d]
    cell2_x, cell2_y = robot.x + 2*SX[robot.d] - DX[robot.d], robot.y + 2*SY[robot.d] - DY[robot.d]
    cell3_x, cell3_y = robot.x + 2*SX[robot.d], robot.y + 2*SY[robot.d]
    return arena.is_obstacle(cell1_x, cell1_y) and arena.is_obstacle(cell2_x, cell2_y) and arena.is_obstacle(cell3_x, cell3_y)


def can_calibrate_left(arena, robot):
    cell1_x, cell1_y = robot.x - 2*SX[robot.d] + DX[robot.d], robot.y - 2*SY[robot.d] + DY[robot.d]
    cell2_x, cell2_y = robot.x - 2*SX[robot.d] - DX[robot.d], robot.y - 2*SY[robot.d] - DY[robot.d]
    cell3_x, cell3_y = robot.x - 2*SX[robot.d], robot.y - 2*SY[robot.d]
    return arena.is_obstacle(cell1_x, cell1_y) and arena.is_obstacle(cell2_x, cell2_y) and arena.is_obstacle(cell3_x, cell3_y)

