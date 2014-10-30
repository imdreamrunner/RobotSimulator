import sys
from conn import Robot
from shortest_path_heuristic import shortest_path
from exploration_heuristic import explore_heuristic
from exploration_lean_wall import explore_lean_wall
from anena import Arena
from constants import *
from sensor_manager import update_known_world, print_sensors
from calibration_manager import can_calibrate_front, can_calibrate_right, can_calibrate_left
import piBluetooth
import jsonpickle
import bluetooth
import threading

visited = [[[0] * 4 for j in range(WIDTH)] for i in range(HEIGHT)]
# Initiate the goal and challenge level
goalX, goalY = 13, 18
challenge = CHALLENGE_EXPLORE_REACH_GOAL
#Count from last calibrate
go_straight_count = 0
move_count = 0
just_finish_kelly_front = False
infinite_loop = False

remain_action = 0


def robot_event_handler(res):
    event = res['event']
    if event == "EXPLORE":
        send_actions([GO_STRAIGHT, 0])
    elif event == "START":
        send_actions([TURN_LEFT, 1])
    elif event == "GET_MAP":
        send_known_world(arena)
    elif event == "TASK_FINISH":
        print "TASK FINISH"
        handle_task_finish(res)
        arena.print_known_world()


def reset_visited():
    global visited, infinite_loop
    visited = [[[False] * 4 for j in range(WIDTH)] for i in range(HEIGHT)]
    infinite_loop = False


def need_calibrate_left_right():
    return just_finish_kelly_front or go_straight_count >= 4 or move_count >= 8


def print_console():
    for x in range(arena.height):
        for y in range(arena.width):
            if x == robot.x and y == robot.y:
                print "@",
            elif arena.map[x][y] == 0:
                print "?",
            elif arena.map[x][y] == 1:
                print ".",
            else:
                print "#",
        print
    print


def handle_task_finish(res):
    global remain_action
    remain_action -= 1
    #Handle only the last task_finish when sending multiple actions
    # print "remain action: ", remain_action
    # if remain_action > 0:
    #     return

    print "Robot position: %d %d %d " % (robot.x, robot.y, robot.d)
    sensors = res['sensors']
    print_sensors(sensors)
    # Update map only in exploration phase
    if challenge < CHALLENGE_RUN_REACH_GOAL:
        update_known_world(arena, robot, sensors)

    print_console()

    action_list = find_next_move()
    send_actions(action_list)


def find_next_move():
    global goalX, goalY, challenge, just_finish_kelly_front, go_straight_count, move_count, infinite_loop
    #Check if reach goal
    if robot.x == goalX and robot.y == goalY:
        #If reach goal
        #Always kelly when reaching goal
        if not just_finish_kelly_front:
            just_finish_kelly_front = True
            return [KELLY, 1]

        challenge += 1
        reset_visited()
        if challenge == CHALLENGE_EXPLORE_REACH_START:
            goalX, goalY = 1, 1
        elif challenge == CHALLENGE_RUN_REACH_GOAL:
            goalX, goalY = 13, 18
            return []
        elif challenge == CHALLENGE_RUN_FINISH:
            arena.print_known_world()
            return []

    #check if can calibrate front
    if (not just_finish_kelly_front) and can_calibrate_front(arena, robot):
        print "calibrate front"
        just_finish_kelly_front = True
        return [KELLY, 1]
    else:
        just_finish_kelly_front = False

    #check if can calibrate_right
    if can_calibrate_right(arena, robot) and need_calibrate_left_right():
        print "calibrate right"
        move_count = 0
        return [TURN_RIGHT, 1, KELLY, 1, TURN_LEFT, 1]

    #check if can calibrate_left
    if can_calibrate_left(arena, robot) and need_calibrate_left_right():
        print "calibrate left"
        move_count = 0
        return [TURN_LEFT, 1, KELLY, 1, TURN_RIGHT, 1]

    #Use algorithm to find the appropriate action
    print "find action using algorithm"
    if challenge == CHALLENGE_EXPLORE_REACH_GOAL:
        action = explore_heuristic(arena, robot, goalX, goalY, visited, challenge)
    elif challenge == CHALLENGE_RUN_REACH_GOAL:
        action = shortest_path(arena, robot, goalX, goalY, visited, challenge)
    else:
        # check if infinite loop
        infinite_loop = infinite_loop or (visited[robot.x][robot.y][robot.d] > 2)
        if infinite_loop:
            action = explore_heuristic(arena, robot, goalX, goalY, visited, challenge)
        else:
            action = explore_lean_wall(arena, robot, goalX, goalY, visited, challenge)

    move_count += 1
    if action == GO_STRAIGHT:
        go_straight_count += 1
    else:
        go_straight_count = 0
    visited[robot.x][robot.y][robot.d] += 1
    return action


def send_actions(action_list):
    global remain_action
    remain_action += len(action_list)/2
    for i in range(len(action_list)):
        if i % 2 == 0:
            action = action_list[i]
            if action == GO_STRAIGHT:
                robot.go_straight(action_list[i+1])
            elif action == TURN_LEFT:
                robot.turn_left()
            elif action == TURN_RIGHT:
                robot.turn_right()
            elif action == KELLY:
                robot.kelly()
            send_known_world(arena)


def send_known_world(arena):
    robot.send_known_world(arena, robot)
    if DISPLAY_MAP:
        mapDisplay.send_known_world(arena, robot)



class androidThread (threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.isRunning = True

    def run(self):
        while True:
            try:
                android.connect()
                while(self.isRunning):
                    receive_string = android.receive()
                    while(receive_string == '' and self.isRunning):
                        print 'is Running'
                        time.sleep(1)
                        receive_string = android.receive()

                    if not self.isRunning:
                        return

                    print 'receiving from android end: ' + receive_string

                    receiveDict = jsonpickle.decode(receive_string)

                    #put with blocking=True
                    #incomingMessageQueue.put(receiveDict, True)
                    event = receiveDict['event']
                    event = event.upper()
                    if event == 'EXPLORE' or event == 'START':
                        robot.send({
                            "event": event
                        })
            except bluetooth.BluetoothError:
                print 'connecting to android failed, retrying'
            except ValueError as msg:
                print msg
            except Exception as msg:
                print msg

android = piBluetooth.PiBluetooth()
androidThreadInstance = androidThread()
androidThreadInstance.start()

#############################################################
arena = Arena(HEIGHT, WIDTH)
robot = Robot("192.168.14.144", 8080, robot_event_handler)
#robot = Robot("127.0.0.1", 8080, robot_event_handler)
mapDisplay = Robot("127.0.0.1", 10200, robot_event_handler)
robot.update_position(7, 9, 1)
robot.start()
if DISPLAY_MAP:
    mapDisplay.start()


while 1:
    s = raw_input()
    if s == 'q':
        androidThreadInstance.isRunning = False
        robot.close()
        sys.exit()
    elif s == "left":
        robot.turn_left()
    elif s == "right":
        robot.turn_right()
    elif s == "go":
        robot.go_straight(1)
    elif s == "explore":
        robot.send({
            "event": "EXPLORE"
        })
    elif s == "start":
        robot.send({
            "event": "START"
        })
    else:
        print "input q to exit."
