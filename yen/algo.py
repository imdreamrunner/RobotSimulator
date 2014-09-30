import sys
from conn import Robot

WIDTH = 20
HEIGHT = 15

robotX = 8
robotY = 10
robotD = 1

state = 1

#challenge = 0: exploration to goal; 1: exploration to start; 2:run
challenge = 0
goalX = 14
goalY = 19

dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]


#free: mark state

def robot_event_handler(res):
    event = res['event']
    if event == "EXPLORE":
        robot.send({
            "event": "ACTION",
            "action": "GO",
            "value": 0.0
        })
    elif event == "START":
        robot.send({
            "event": "ACTION",
            "action": "GO",
            "value": 0.0
        })
    elif event == "TASK_FINISH":
        print "TASK FINISH"
        handle_task_finish(res)


def handle_task_finish(res):
    global robotX, robotY, goalX, goalY, challenge
    print "Robot position: %d %d %d " % (robotX, robotY, robotD)
    #Check if reach goal
    if robotX == goalX and robotY == goalY:
        #If reach goal
        challenge += 1
        if challenge == 1:
            goalX, goalY = 2, 2
        elif challenge == 2:
            goalX = 14
            goalY = 19
            print "return"
            return
        elif challenge == 3:
            print "return"
            return

    sensors = res['sensors']
    global s_front_mid, s_front_left, s_front_right
    s_front_mid = sensors[0]
    s_front_left = sensors[1]
    s_front_right = sensors[2]
    s_left = sensors[3]
    s_right = sensors[4]
    no_obstacle_ahead = (s_front_left > 10) and (s_front_mid > 10) and (s_front_right > 10)
    no_obstacle_mid_left = (s_left > 10)
    no_obstacle_mid_right = (s_right > 10)

    global state
    if state == 0 and no_obstacle_mid_right:
     #and ((not no_obstacle_ahead) or distance_to_goal(robotX + dx[robotD], robotY + dy[robotD]) >= distance_to_goal(robotX + dx[right(robotD)], robotY + dy[right(robotD)])):
        turn_right()
        state = 1
    else:
        if no_obstacle_ahead:
            #and ((not no_obstacle_mid_left) or distance_to_goal(robotX + dx[robotD], robotY + dy[robotD]) <= distance_to_goal(robotX + dx[left(robotD)], robotY + dy[left(robotD)])):
            go_straight(1)
            state = 0
        else:
            if no_obstacle_mid_left:
                turn_left()
                state = 1
            else:
                turn_left()
                turn_left()
                state = 1


def distance_to_goal(x, y):
    return abs(goalX - x) + abs(goalY - y)


def get_grid(x, y, d, dd):
    x += dx[d]*dd
    y += dy[d]*dd
    return x, y


def left(d):
    return (d+3) % 4


def right(d):
    return (d+1) % 4


def go_straight(unit):
    print "go straight"
    global robotX, robotY, robotD
    robotX, robotY = get_grid(robotX, robotY, robotD, unit)

    robot.send({
        "event": "ACTION",
        "action": "GO",
        "value": 10.0 * unit
    })


def turn_left():
    print "turn left"
    global robotD
    robotD = left(robotD)
    robot.send({
        "event": "ACTION",
        "action": "ROTATE",
        "value": -0.25
    })


def turn_right():
    print "turn right"
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
