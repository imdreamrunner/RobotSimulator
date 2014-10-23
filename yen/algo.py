import os
import sys
from conn import Robot
from path_finder_yen import explore

DISPLAY_MAP = False
WIDTH = 20
HEIGHT = 15

DX = [-1, 0, 1, 0]
DY = [0, 1, 0, -1]
sx = [0, 1, 0, -1]
sy = [1, 0, -1, 0]

CHALLENGE_EXPLORE_REACH_GOAL = 0
CHALLENGE_EXPLORE_REACH_START = 1
CHALLENGE_RUN_REACH_GOAL = 2
CHALLENGE_RUN_FINISH = 3

robotX, robotY, robotD = 7, 9, 1
goalX, goalY = 13, 18
challenge = CHALLENGE_EXPLORE_REACH_GOAL
just_finish_kelly = False

knownWorld = [[0] * WIDTH for i in range(HEIGHT)]


def robot_event_handler(res):
    event = res['event']
    if event == "EXPLORE":
        turn_right()
    elif event == "START":
        turn_left()
    elif event == "GET_MAP":
        send_known_world()
    elif event == "TASK_FINISH":
        print "TASK FINISH"
        handle_task_finish(res)
        send_known_world()


def is_outside(x, y):
    return x < 0 or x >= HEIGHT or y < 0 or y >= WIDTH


def update_known_cell(x, y, val):
    if is_outside(x, y):
        return
    knownWorld[x][y] = val


def update_known_cell_from_sensor(x, y, direction, distance):
    if distance > 50:
        distance = 50

    if distance > 45:
        no_obstacle = True
    else:
        no_obstacle = False

    while distance > -10:
        update_known_cell(x, y, 1)
        x, y = get_grid(x, y, direction, 1)
        distance -= 10

    if not no_obstacle:
        update_known_cell(x, y, 2)


def update_known_world(sensors):
    # 8 cell around robot marked free
    for i in range(3):
        for j in range(3):
            update_known_cell(robotX+i-1, robotY+j-1, 1)

    s_front_mid = sensors[0]
    s_front_left = sensors[1]
    s_front_right = sensors[2]
    s_left = sensors[3]
    s_right = sensors[4]

    # if s_front_left > 10 and s_front_right > 10:
    #     # update_known_cell_from_sensor(robotX, robotY, robotD, min(s_front_left, s_front_right))
    #     update_known_cell(robotX + DX[robotD], robotY + DY[robotD], 1)
    #     update_known_cell(robotX + DX[robotD]*2, robotY + DY[robotD]*2, 1)
    update_known_cell_from_sensor(robotX, robotY, robotD, s_front_mid)
    update_known_cell_from_sensor(robotX, robotY, right(robotD), s_right)
    update_known_cell_from_sensor(robotX, robotY, left(robotD), s_left)
    update_known_cell_from_sensor(robotX-sx[robotD], robotY-sy[robotD], robotD, s_front_left)
    update_known_cell_from_sensor(robotX+sx[robotD], robotY+sy[robotD], robotD, s_front_right)


def face_wall(sensors):
    s_front_mid = sensors[0]
    s_front_left = sensors[1]
    s_front_right = sensors[2]
    return s_front_left < 10 and s_front_right < 10
    # fw = int(s_front_mid < 10) + int(s_front_left < 10) + int(s_front_right < 10)
    # return fw >= 2


def handle_task_finish(res):
    global robotX,  robotY, goalX, goalY, challenge, new_challenge, just_finish_kelly
    print "Robot position: %d %d %d " % (robotX, robotY, robotD)
    sensors = res['sensors']
    print_known_world_console()
    update_known_world(sensors)

    #Check if reach goal
    if robotX == goalX and robotY == goalY:
        #If reach goal
        challenge += 1
        if challenge == CHALLENGE_EXPLORE_REACH_START:
            goalX, goalY = 1, 1
        elif challenge == CHALLENGE_RUN_REACH_GOAL:
            goalX, goalY = 13, 18
            print_known_world()
            return
        elif challenge == CHALLENGE_RUN_FINISH:
            print_known_world()
            return

    #check if face wall, callibrate
    if (not just_finish_kelly) and face_wall(sensors):
        print robotX, robotY, robotD
        kelly()
        just_finish_kelly = True
    else:
        just_finish_kelly = False
        action = explore(knownWorld, robotX, robotY, robotD, goalX, goalY, challenge)
        if action == 0:
            go_straight(1)
        elif action == 3:
            turn_left()
        else:
            turn_right()


def print_known_world_console():
    for x in range(HEIGHT):
        for y in range(WIDTH):
            print "%2d" %(knownWorld[x][y]),
        print
    print


def print_known_world():

    os.system('cls')    # windows
    # os.system('clear')  # linux

    expl = 0b11
    obst = 0xF

    for w in range(WIDTH):
        for h in range(HEIGHT):
            print knownWorld[h][WIDTH - w - 1],
            # print knownWorld[w][h],
            expl <<= 1
            if knownWorld[h][w] > 0:
                expl |= 0b1
                obst <<= 1
                if knownWorld[h][w] == 2:
                    obst |= 0b1
        print
    print
    expl <<= 2
    expl |= 0b11

    if obst.bit_length() % 4 != 0:
        obst <<= 4 - obst.bit_length() % 4
    obst_string = format(obst, "X")[1:]

    print "Explored:", format(expl, "X")
    print "Obstacle:", obst_string
    print


def send_known_world():
    stri = ""
    for w in range(WIDTH-1, -1, -1):
        for h in range(HEIGHT):
            stri += str(knownWorld[h][w])

    map_data = {
        "event": "MAP",
        "map_info": stri,
        "location_y": WIDTH - robotY - 1,
        "location_x": robotX,
        "direction": right(right(robotD))
    }

    robot.send(map_data)
    if DISPLAY_MAP:
        mapDisplay.send(map_data)


def get_grid(x, y, d, dd):
    newx = x + DX[d] * dd
    newy = y + DY[d] * dd
    return newx, newy


def go_straight(unit):
    global robotX, robotY, robotD
    robotX, robotY = get_grid(robotX, robotY, robotD, unit)
    robot.send({
        "event": "ACTION",
        "action": "GO",
        "quantity": unit
    })


def turn_left():
    global robotD
    robotD = left(robotD)
    robot.send({
        "event": "ACTION",
        "action": "ROTATE",
        "quantity": -1
    })


def turn_right():
    global robotD
    robotD = right(robotD)
    robot.send({
        "event": "ACTION",
        "action": "ROTATE",
        "quantity": 1
    })


def kelly():
    robot.send({
        "event": "ACTION",
        "action": "KELLY"
    })


def left(d):
    return (d+3) % 4


def right(d):
    return (d+1) % 4


robot = Robot("192.168.14.144", 8080, robot_event_handler)
# robot = Robot("127.0.0.1", 8080, robot_event_handler)
mapDisplay = Robot("127.0.0.1", 10200, robot_event_handler)

robot.start()
if DISPLAY_MAP:
    mapDisplay.start()


while 1:
    s = raw_input()
    if s == 'q':
        robot.close()
        sys.exit()
    elif s == "left":
        turn_left()
    elif s == "right":
        turn_right()
    elif s == "go":
        go_straight(1)
    elif s == "explore":
        robot.send({
            "event": "EXPLORE"
        })
    else:
        print "input q to exit."
