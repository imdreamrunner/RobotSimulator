import sys
from conn import Robot

WIDTH = 20
HEIGHT = 15

robotX = 9
robotY = 7
robotD = 1

state = 1


def robot_event_handler(res):
    event = res['event']
    if event == "EXPLORE":
        robot.send({
            "event": "ACTION",
            "action": "GO",
            "value": 10.0
        })
    elif event == "START":
        pass
    elif event == "TASK_FINISH":
        print "TASK FINISH"
        sensors = res['sensors']
        global s_front_mid, s_front_left, s_front_right
        s_front_mid = sensors[0]
        s_front_left = sensors[1]
        s_front_right = sensors[2]
        s_left = sensors[3]
        s_right = sensors[4]
        no_obstacle_ahead = (s_front_left > 10) and (s_front_mid > 10) and (s_front_right > 10)

        global state
        if state == 0:
            turn_left()
            state = 1
        elif state == 1:
            if no_obstacle_ahead:
                go_straight(1)
                state = 0
            else:
                turn_right()
                state = 1


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
        robot.send({
            "event": "ACTION",
            "action": "GO",
            "value": 10.0
        })
