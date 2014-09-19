# A very slow but accurate algorithm.

import sys
from conn import Robot
from path_finder import find_path


WIDTH = 20
HEIGHT = 15

robotX = 9
robotY = 7
robotD = 0

knownWorld = [[0 for j in range(HEIGHT)] for i in range(WIDTH)]
# 0 for unknown 1 for free and 2 for obstacles

toStart = False


def set_world(x, y, value):
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        knownWorld[x][y] = value


def left(d):
    return (d+3) % 4


def right(d):
    return (d+1) % 4


def get_grid(x, y, d, dd):
    if d == 0:
        x += dd
    elif d == 1:
        y += dd
    elif d == 2:
        x -= dd
    elif d == 3:
        y -= dd
    return x, y


def robot_event_handler(res):
    event = res['event']
    if event == "EXPLORE":
        robot.send({
            "event": "ACTION",
            "action": "GO",
            "value": 0
        })
    elif event == "START":
        pass
    elif event == "TASK_FINISH":
        sensors = res['sensors']
        s_front_mid = sensors[0]
        s_front_left = sensors[1]
        s_front_right = sensors[2]
        s_left = sensors[3]
        s_right = sensors[4]
        # Front Mid
        s_tmp = s_front_mid
        g_tmp = 1
        while s_tmp > 10:
            x, y = get_grid(robotX, robotY, robotD, g_tmp+1)
            set_world(x, y, 1)
            g_tmp += 1
            s_tmp -= 10
        if g_tmp < 8:
            x, y = get_grid(robotX, robotY, robotD, g_tmp+1)
            set_world(x, y, 2)
        # Front Left
        s_tmp = s_front_left
        g_tmp = 1
        r_x, r_y = get_grid(robotX, robotY, left(robotD), 1)
        while s_tmp > 10:
            x, y = get_grid(r_x, r_y, robotD, g_tmp+1)
            set_world(x, y, 1)
            g_tmp += 1
            s_tmp -= 10
        if g_tmp < 8:
            x, y = get_grid(r_x, r_y, robotD, g_tmp+1)
            set_world(x, y, 2)
        # Front Right
        s_tmp = s_front_right
        g_tmp = 1
        r_x, r_y = get_grid(robotX, robotY, right(robotD), 1)
        while s_tmp > 10:
            x, y = get_grid(r_x, r_y, robotD, g_tmp+1)
            set_world(x, y, 1)
            g_tmp += 1
            s_tmp -= 10
        if g_tmp < 8:
            x, y = get_grid(r_x, r_y, robotD, g_tmp+1)
            set_world(x, y, 2)
        # Left
        s_tmp = s_left
        g_tmp = 1
        while s_tmp > 10:
            x, y = get_grid(robotX, robotY, left(robotD), g_tmp+1)
            set_world(x, y, 1)
            g_tmp += 1
            s_tmp -= 10
        if g_tmp < 8:
            x, y = get_grid(robotX, robotY, left(robotD), g_tmp+1)
            set_world(x, y, 2)
        # Right
        s_tmp = s_right
        g_tmp = 1
        while s_tmp > 10:
            x, y = get_grid(robotX, robotY, right(robotD), g_tmp+1)
            set_world(x, y, 1)
            g_tmp += 1
            s_tmp -= 10
        if g_tmp < 8:
            x, y = get_grid(robotX, robotY, right(robotD), g_tmp+1)
            set_world(x, y, 2)
        print_known_world()
        global toStart
        if robotX == WIDTH - 2 and robotY == HEIGHT - 2:
            print "Reach goal"
            toStart = True
        elif robotX == 1 and robotY == 1:
            print "Reach start"
            sys.exit(0)

        if toStart:
            action = find_path(knownWorld, robotX, robotY, robotD, 1, 1)
        else:
            action = find_path(knownWorld, robotX, robotY, robotD, WIDTH - 2, HEIGHT - 2)
        print action
        if action == "straight":
            go_straight(1)
        elif action == "left":
            turn_left()
        elif action == "right":
            turn_right()


def print_known_world():
    for j in range(HEIGHT):
        for i in range(WIDTH):
            print knownWorld[i][j],
        print
    print


def go_straight(unit):
    global robotX, robotY, robotD
    robotX, robotY = get_grid(robotX, robotY, robotD, unit)
    robot.send({
        "event": "ACTION",
        "action": "GO",
        "value": 10.0 * unit
    })


def turn_left():
    global robotD
    robotD = left(robotD)
    robot.send({
        "event": "ACTION",
        "action": "ROTATE",
        "value": -0.25
    })


def turn_right():
    global robotD
    robotD = right(robotD)
    robot.send({
        "event": "ACTION",
        "action": "ROTATE",
        "value": 0.25
    })

robot = Robot("127.0.0.1", 8888, robot_event_handler)

robot.start()

while 1:
    s = raw_input()
    if s == 'q':
        robot.close()
        sys.exit()
    else:
        print "input q to exit."