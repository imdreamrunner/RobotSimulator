import os
import sys
from conn import Robot
from shortest_path_heuristic import shortest_path
from exploration_heuristic import explore_heuristic
from exploration_lean_wall import explore_lean_wall

DISPLAY_MAP = False
WIDTH = 20
HEIGHT = 15

DX = [-1, 0, 1, 0]
DY = [0, 1, 0, -1]
SX = [0, 1, 0, -1]
SY = [1, 0, -1, 0]

CHALLENGE_EXPLORE_REACH_GOAL = 0
CHALLENGE_EXPLORE_REACH_START = 1
CHALLENGE_RUN_REACH_GOAL = 2
CHALLENGE_RUN_FINISH = 3

GO_STRAIGHT = 0
TURN_RIGHT = 1
TURN_LEFT = 3

knownWorld = [[0] * WIDTH for i in range(HEIGHT)]
visited = [[[0] * 4 for j in range(WIDTH)] for i in range(HEIGHT)]

robotX, robotY, robotD = 7, 9, 1
goalX, goalY = 13, 18
challenge = CHALLENGE_EXPLORE_REACH_GOAL
#Count from last calibrate
go_straight_count = 0
move_count = 0
infinite_loop = False
just_finish_kelly_front = False


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
        # print_known_world()


def reset_visited():
    global visited, infinite_loop
    visited = [[[False] * 4 for j in range(WIDTH)] for i in range(HEIGHT)]
    infinite_loop = False


def is_outside(x, y):
    return x < 0 or x >= HEIGHT or y < 0 or y >= WIDTH


def is_obstacle(known_world, x, y):
    if is_outside(x, y):
        return True
    return known_world[x][y] == 2


def update_known_cell(x, y, val):
    if is_outside(x, y):
        return
    knownWorld[x][y] = val


def update_known_cell_from_sensor(x, y, direction, distance):
    if distance > 32:
        distance = 32

    if distance > 30:
        no_obstacle = True
    else:
        no_obstacle = False

    x, y = get_grid(x, y, direction, 1)

    while distance > 2:
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

    update_known_cell_from_sensor(robotX, robotY, robotD, s_front_mid)
    update_known_cell_from_sensor(robotX, robotY, right(robotD), s_right)
    update_known_cell_from_sensor(robotX, robotY, left(robotD), s_left)
    update_known_cell_from_sensor(robotX-SX[robotD], robotY-SY[robotD], robotD, s_front_left)
    update_known_cell_from_sensor(robotX+SX[robotD], robotY+SY[robotD], robotD, s_front_right)


def face_wall(sensors):
    cell1_x, cell1_y = robotX + SX[robotD] + 2*DX[robotD], robotY + SY[robotD] + 2*DY[robotD]
    cell2_x, cell2_y = robotX - SX[robotD] + 2*DX[robotD], robotY - SY[robotD] + 2*DY[robotD]
    return is_obstacle(knownWorld, cell1_x, cell1_y) and is_obstacle(knownWorld, cell2_x, cell2_y)


def need_calibrate_left_right():
    return just_finish_kelly_front or go_straight_count >= 3 or move_count >= 6


def can_calibrate_right():
    cell1_x, cell1_y = robotX + 2*SX[robotD] + DX[robotD], robotY + 2*SY[robotD] + DY[robotD]
    cell2_x, cell2_y = robotX + 2*SX[robotD] - DX[robotD], robotY + 2*SY[robotD] - DY[robotD]
    return is_obstacle(knownWorld, cell1_x, cell1_y) and is_obstacle(knownWorld, cell2_x, cell2_y)


def can_calibrate_left():
    cell1_x, cell1_y = robotX - 2*SX[robotD] + DX[robotD], robotY - 2*SY[robotD] + DY[robotD]
    cell2_x, cell2_y = robotX - 2*SX[robotD] - DX[robotD], robotY - 2*SY[robotD] - DY[robotD]
    return is_obstacle(knownWorld, cell1_x, cell1_y) and is_obstacle(knownWorld, cell2_x, cell2_y)


def can_calibrate_front(sensors):
    return face_wall(sensors)


def handle_task_finish(res):
    global goalX, goalY, challenge, just_finish_kelly_front, go_straight_count, move_count, infinite_loop

    print "Robot position: %d %d %d " % (robotX, robotY, robotD)
    sensors = res['sensors']
    print "Sensors: ", sensors[0], sensors[1], sensors[2], sensors[3], sensors[4]

    # print_known_world_console()
    update_known_world(sensors)

    #Check if reach goal
    if robotX == goalX and robotY == goalY:
        #If reach goal
        challenge += 1
        reset_visited()
        if challenge == CHALLENGE_EXPLORE_REACH_START:
            goalX, goalY = 1, 1
        elif challenge == CHALLENGE_RUN_REACH_GOAL:
            goalX, goalY = 13, 18
            print_known_world()
            return
        elif challenge == CHALLENGE_RUN_FINISH:
            print_known_world()
            return

    #check if can calibrate front
    if (not just_finish_kelly_front) and can_calibrate_front(sensors):
        print "calibrate front"
        kelly()
        just_finish_kelly_front = True
        return
    else:
        just_finish_kelly_front = False

    #check if can calibrate_right
    if can_calibrate_right() and need_calibrate_left_right():
        print "calibrate right"
        turn_right()
        kelly()
        turn_left()
        return

    #check if can calibrate_left
    if can_calibrate_left() and need_calibrate_left_right():
        print "calibrate left"
        turn_left()
        kelly()
        turn_right()
        return

    #Use algorithm to find the appropriate action
    print "find action using algorithm"
    if challenge == CHALLENGE_RUN_REACH_GOAL:
        action = shortest_path(knownWorld, robotX, robotY, robotD, goalX, goalY, visited, challenge)
    else:
        # check if infinite loop
        infinite_loop = infinite_loop or (visited[robotX][robotY][robotD] > 2)
        if infinite_loop:
            action = explore_heuristic(knownWorld, robotX, robotY, robotD, goalX, goalY, visited, challenge)
        else:
            action = explore_lean_wall(knownWorld, robotX, robotY, robotD, goalX, goalY, visited, challenge)

    move_count += 1
    if action == GO_STRAIGHT:
        go_straight(1)
        go_straight_count += 1
    else:
        go_straight_count = 0
        if action == TURN_LEFT:
            turn_left()
        else:
            turn_right()
    visited[robotX][robotY][robotD] += 1


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
    global go_straight_count, move_count
    robot.send({
        "event": "ACTION",
        "action": "KELLY"
    })
    go_straight_count = 0
    move_count = 0


def left(d):
    return (d+3) % 4


def right(d):
    return (d+1) % 4


# robot = Robot("192.168.14.144", 8080, robot_event_handler)
robot = Robot("127.0.0.1", 8080, robot_event_handler)
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
