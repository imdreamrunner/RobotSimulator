# A very slow but accurate algorithm.

import sys
import os
import time
from conn import Robot
from path_finder import find_path
from util import *


WIDTH = 20
HEIGHT = 15

robotX = 9
robotY = 7
robotD = 0

arena_file = open("arena.txt")

knownWorld = [[0 for j in range(HEIGHT)] for i in range(WIDTH)]

for i in range(HEIGHT):
    knownWorldLine = []
    line = arena_file.readline()[:-1]
    for j in range(WIDTH):
        knownWorld[j][i] = int(line[j]) + 1

print knownWorld

goalPoint = 0
# 0 to goal, 1 to start, 2 shortest preparation, 3 wait for start, 4 fastest run
explored_start_time = 0.0
path_list = []


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
    global goalPoint, path_list, explored_start_time
    event = res['event']
    if event == "EXPLORE":
        explored_start_time = time.time()
        go_straight(0)
    elif event == "START":
        # start fastest run
        goalPoint = 4
        if len(path_list) == 0:
            print "done"
            return
        action = path_list.pop(0)
        print action
        if action == "straight":
            go_straight(1)
        elif action == "left":
            turn_left()
        elif action == "right":
            turn_right()
    elif event == "GET_MAP":
        send_know_world()
    elif event == "TASK_FINISH":
        action = None

        if goalPoint < 2:
            time_length = time.time() - explored_start_time
            coverage = get_coverage(knownWorld, WIDTH, HEIGHT) * 100
            print "Exploration time:", time_length, "s"
            print "Exploration coverage:", coverage, "%"
            print
        if goalPoint == 0:
            if robotX == WIDTH - 2 and robotY == HEIGHT - 2:
                print "Reach goal"
                goalPoint = 1
            else:
                action = find_path(knownWorld, robotX, robotY, robotD, WIDTH - 2, HEIGHT - 2)
        if goalPoint == 1:
            if robotX == 1 and robotY == 1:
                print "Reach start"
                goalPoint = 2
            else:
                action = find_path(knownWorld, robotX, robotY, robotD, 1, 1)
        if goalPoint == 2:
            if len(path_list) == 0:
                from shortest_path import find_path_list
                path_list = find_path_list(knownWorld, robotX, robotY, robotD, WIDTH - 2, HEIGHT - 2)
            if path_list[0] != "straight":
                action = path_list.pop(0)
            else:
                goalPoint = 3
        if goalPoint == 4:
            if len(path_list) > 0:
                action = path_list.pop(0)
            else:
                print "done"
        if action is None:
            return
        print "Next step:", action
        if action == "straight":
            go_straight(1)
        elif action == "left":
            turn_left()
        elif action == "right":
            turn_right()

        send_know_world()


def print_known_world():
    os.system('cls')    # windows
    os.system('clear')  # linux
    explored_string, obstacle_string = get_hex_map(knownWorld, WIDTH, HEIGHT)
    print "Explored:", explored_string
    print "Obstacle:", obstacle_string
    print


def send_know_world():
    stri = ""
    for w in range(WIDTH-1, -1, -1):
        for h in range(HEIGHT):
            stri += str(knownWorld[w][h])
    robot.send({
        "event": "MAP",
        "map_info": stri,
        "location_x": HEIGHT - robotY,
        "location_y": robotX + 1,
        "direction": left(robotD)
    })


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

# robot = Robot("172.22.94.108", 8080, robot_event_handler)
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