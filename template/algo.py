import sys
from conn import Robot


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
        s_front_mid = sensors[0]
        s_front_left = sensors[1]
        s_front_right = sensors[2]
        s_left = sensors[3]
        s_right = sensors[4]


def go_straight(unit):
    robot.send({
        "event": "ACTION",
        "action": "GO",
        "value": 10.0 * unit
    })


def turn_left():
    robot.send({
        "event": "ACTION",
        "action": "ROTATE",
        "value": -0.25
    })


def turn_right():
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
