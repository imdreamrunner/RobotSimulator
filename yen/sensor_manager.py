from utils import *


def print_sensors(sensors):
    print "Sensors: ", sensors[0], sensors[1], sensors[2], sensors[3], sensors[4]


def update_known_cell_from_sensor(arena, x, y, direction, distance):
    if distance > 32:
        distance = 32

    if distance > 30:
        no_obstacle = True
    else:
        no_obstacle = False

    x, y = get_grid(x, y, direction, 1)

    while distance > 2:
        arena.update_known_cell(x, y, 1)
        x, y = get_grid(x, y, direction, 1)
        distance -= 10

    if not no_obstacle:
        arena.update_known_cell(x, y, 2)


def update_known_world(arena, robot, sensors):
    # 8 cell around robot marked free
    for i in range(3):
        for j in range(3):
            arena.update_known_cell(robot.x + i - 1, robot.y + j - 1, 1)

    s_front_mid = sensors[0]
    s_front_left = sensors[1]
    s_front_right = sensors[2]
    s_left = sensors[3]
    s_right = sensors[4]

    update_known_cell_from_sensor(arena, robot.x, robot.y, robot.d, s_front_mid)
    update_known_cell_from_sensor(arena, robot.x, robot.y, right(robot.d), s_right)
    update_known_cell_from_sensor(arena, robot.x, robot.y, left(robot.d), s_left)
    update_known_cell_from_sensor(arena, robot.x-SX[robot.d], robot.y-SY[robot.d], robot.d, s_front_left)
    update_known_cell_from_sensor(arena, robot.x+SX[robot.d], robot.y+SY[robot.d], robot.d, s_front_right)

