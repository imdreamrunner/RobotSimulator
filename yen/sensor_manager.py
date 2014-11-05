from constants import *

MIN_FRONT = 5
MIN_LEFT = 0


def print_sensors(sensors):
    print "Sensors: ", sensors[0], sensors[1], sensors[2], sensors[3], sensors[4]


def update_known_cell_from_sensor(arena, x, y, direction, distance, min_dis):
    max_distance_sense = min_dis + 20

    if distance >= max_distance_sense + 1:
        distance = max_distance_sense + 1

    if distance > max_distance_sense:
        no_obstacle = True
    else:
        no_obstacle = False

    x, y = get_grid(x, y, direction, 1)

    while distance >= min_dis:
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

    update_known_cell_from_sensor(arena, robot.x, robot.y, robot.d, s_front_mid, MIN_FRONT)
    update_known_cell_from_sensor(arena, robot.x, robot.y, right(robot.d), s_right, MIN_FRONT)
    update_known_cell_from_sensor(arena, robot.x, robot.y, left(robot.d), s_left, MIN_FRONT)
    update_known_cell_from_sensor(arena, robot.x-SX[robot.d], robot.y-SY[robot.d], robot.d, s_front_left, MIN_LEFT)
    update_known_cell_from_sensor(arena, robot.x+SX[robot.d], robot.y+SY[robot.d], robot.d, s_front_right, MIN_LEFT)

