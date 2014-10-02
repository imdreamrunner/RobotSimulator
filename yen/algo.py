import os
import sys
from conn import Robot
from new_path_finder import explore

WIDTH = 20
HEIGHT = 15
challenge = 0
robotX, robotY, robotD = 7, 9, 1
goalX, goalY = 13, 18

dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]
sx = [0, 1, 0, -1]
sy = [1, 0, -1, 0]

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


def is_outside(x, y):
    return x < 0 or x >= HEIGHT or y < 0 or y >= WIDTH


def update_known_cell(x, y, val):
    if is_outside(x, y):
        return
    knownWorld[x][y] = val


def update_known_cell_from_sensor(x, y, direction, distance):
    while distance > -10:
        update_known_cell(x, y, 1)
        x, y = get_grid(x, y, direction, 1)
        distance -= 10
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

    update_known_cell_from_sensor(robotX, robotY, robotD, s_front_mid)
    update_known_cell_from_sensor(robotX, robotY, right(robotD), s_right)
    update_known_cell_from_sensor(robotX, robotY, left(robotD), s_left)
    update_known_cell_from_sensor(robotX-sx[robotD], robotY-sy[robotD], robotD, s_front_left)
    update_known_cell_from_sensor(robotX+sx[robotD], robotY+sy[robotD], robotD, s_front_right)


def handle_task_finish(res):
    global robotX,  robotY, goalX, goalY, challenge, visited, state
    print "Robot position: %d %d %d " % (robotX, robotY, robotD)
    sensors = res['sensors']
    print "sensors: %d %d %d %d %d" %(sensors[0], sensors[1], sensors[2], sensors[3], sensors[4])

    update_known_world(sensors)

    #Check if reach goal
    if robotX == goalX and robotY == goalY:
        #If reach goal
        challenge += 1
        if challenge == 1:
            goalX, goalY = 1, 1
        elif challenge == 2:
            goalX, goalY = 13, 18
            print_known_world()
            print "return"
            return
        elif challenge == 3:
            print_known_world()
            print "return"
            return

    action = explore(knownWorld, robotX, robotY, robotD, goalX, goalY)
    if action == 0:
        go_straight(1)
    elif action == 3:
        turn_left()
    else:
        turn_right()


def print_known_world():

    # for x in range(HEIGHT):
    #     for y in range(WIDTH):
    #         print "%3d" %(knownWorld[x][y]),
    #     print
    # print
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
    robot.send({
        "event": "MAP",
        "map_info": stri,
        "location_x": HEIGHT - robotY,
        "location_y": robotX + 1,
        "direction": left(robotD)
    })


def get_grid(x, y, d, dd):
    newx = x + dx[d] * dd
    newy = y + dy[d] * dd
    return newx, newy


def left(d):
    return (d+3) % 4


def right(d):
    return (d+1) % 4


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

robot = Robot("127.0.0.1", 8888, robot_event_handler)

robot.start()

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
