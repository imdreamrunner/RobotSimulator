import sys
from conn import Robot
from shortest_path_heuristic import ShortestPathHeuristic
from exploration_heuristic import ExplorationHeuristic
from exploration_lean_wall import ExplorationLeanWall
from shortest_path_bfs import ShortestPathBFS
from anena import Arena
from constants import *
from sensor_manager import update_known_world, print_sensors
from calibration_manager import can_calibrate_front, can_calibrate_right, can_calibrate_left
from queue import Queue, Task
# import piBluetooth
# import jsonpickle
# import bluetooth
# import threading

visited = [[[0] * 4 for j in range(WIDTH)] for i in range(HEIGHT)]
# Initiate the goal and challenge level
goalX, goalY = 13, 18
challenge = CHALLENGE_EXPLORE_REACH_GOAL
#Count from last calibrate
go_straight_count = 0
move_count = 0
just_finish_kelly_front = False
infinite_loop = False

#Algorithm strategy
exploration_heuristic_algo = ExplorationHeuristic()
exploration_leanwall_algo = ExplorationLeanWall()
shortest_path_heuristic_algo = ShortestPathHeuristic()
shortest_path_bfs_algo = ShortestPathBFS()

algo = exploration_heuristic_algo
task_queue = Queue()


def robot_event_handler(res):
    event = res['event']
    if event == "EXPLORE":
        send_task(Task(GO_STRAIGHT, 0))
    elif event == "START":
        send_task(Task(GO_STRAIGHT, 0))
    elif event == "GET_MAP":
        send_known_world(arena)
    elif event == "TASK_FINISH":
        print "TASK FINISH"
        handle_task_finish(res)
        arena.print_known_world()


def init_challenge():
    global task_queue, visited, infinite_loop
    visited = [[[False] * 4 for j in range(WIDTH)] for i in range(HEIGHT)]
    infinite_loop = False
    if challenge == CHALLENGE_RUN_REACH_GOAL:
        task_queue = Queue()


def handle_task_finish(res):
    global task_queue

    if task_queue.isEmpty():
        # if task_queue empty, find next tasks need to be performed
        print "Robot position: %d %d %d " % (robot.x, robot.y, robot.d)
        sensors = res['sensors']
        print_sensors(sensors)
        update_known_world(arena, robot, sensors)
        print_console()
        task_queue.enqueue_list(find_next_move())
    if not task_queue.isEmpty():
        send_task(task_queue.dequeue())


def send_task(task):
    global go_straight_count, move_count
    action = task.action
    quantity = task.quantity
    if action == GO_STRAIGHT:
        robot.go_straight(quantity)
    elif action == TURN_LEFT:
        robot.turn_left()
    elif action == TURN_RIGHT:
        robot.turn_right()
    elif action == KELLY:
        robot.kelly()
        # update calibration move count
        go_straight_count = 0
        move_count = 0
        # update last kelly

    if action == GO_STRAIGHT:
        go_straight_count += quantity
    else:
        go_straight_count = 0
    send_known_world(arena)


def need_calibrate_left_right():
    if challenge == CHALLENGE_RUN_REACH_GOAL:
        return False
    # return just_finish_kelly_front or \
    return go_straight_count >= 4 or move_count >= 6


def find_next_move():
    """
    Return a list of action the robot should perform next
    """
    global goalX, goalY, challenge, just_finish_kelly_front, go_straight_count, move_count, infinite_loop, algo
    #Check if reach goal
    if robot.x == goalX and robot.y == goalY:
        #If reach goal
        #Always kelly when reaching goal
        if not just_finish_kelly_front:
            just_finish_kelly_front = True
            return [Task(KELLY, 1)]

        challenge += 1
        if challenge == CHALLENGE_EXPLORE_REACH_START:
            init_challenge()
            goalX, goalY = 1, 1
        elif challenge == CHALLENGE_RUN_REACH_GOAL:
            if robot.d == 3:
                challenge -= 1
                # return [Task(TURN_RIGHT, 1), Task(KELLY, 1), Task(TURN_RIGHT, 1)]
                return [Task(TURN_LEFT, 1)]
            elif robot.d == 4:
                challenge -= 1
                return [Task(TURN_RIGHT, 1)]
            init_challenge()
            goalX, goalY = 13, 18
            return []
        elif challenge == CHALLENGE_RUN_FINISH:
            arena.print_known_world()
            return []

    #check if can calibrate front
    if (not just_finish_kelly_front) and can_calibrate_front(arena, robot):
        print "calibrate front"
        just_finish_kelly_front = True
        return [Task(KELLY, 1)]
    else:
        just_finish_kelly_front = False

    #check if can calibrate_right
    if can_calibrate_right(arena, robot) and need_calibrate_left_right():
        print "calibrate right"
        return [Task(TURN_RIGHT, 1), Task(KELLY, 1), Task(TURN_LEFT, 1)]

    #check if can calibrate_left
    if can_calibrate_left(arena, robot) and need_calibrate_left_right():
        print "calibrate left"
        return [Task(TURN_LEFT, 1), Task(KELLY, 1), Task(TURN_RIGHT, 1)]

    #Use algorithm to find the appropriate action
    print "find action using algorithm"
    if challenge == CHALLENGE_RUN_REACH_GOAL:
        #algo = shortest_path_bfs_algo
        algo = shortest_path_heuristic_algo
    elif challenge == CHALLENGE_EXPLORE_REACH_GOAL:
        algo = exploration_heuristic_algo
    else:
        # check if infinite loop
        infinite_loop = infinite_loop or (visited[robot.x][robot.y][robot.d] > 2)
        if infinite_loop:
            algo = exploration_heuristic_algo
        else:
            algo = exploration_leanwall_algo
    action_list = algo.run(arena, robot, goalX, goalY, visited, challenge)
    print "Action: ",
    for action in action_list:
        print "[", action.action, action.quantity, "]"
    move_count += 1
    visited[robot.x][robot.y][robot.d] += 1
    return action_list


def send_known_world(arena):
    robot.send_known_world(arena, robot)
    if DISPLAY_MAP:
        mapDisplay.send_known_world(arena, robot)


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

# class androidThread (threading.Thread):
#
#     def __init__(self):
#         threading.Thread.__init__(self)
#         self.isRunning = True
#
#     def run(self):
#         while True:
#             try:
#                 android.connect()
#                 while(self.isRunning):
#                     receive_string = android.receive()
#                     while(receive_string == '' and self.isRunning):
#                         print 'is Running'
#                         time.sleep(1)
#                         receive_string = android.receive()
#
#                     if not self.isRunning:
#                         return
#
#                     print 'receiving from android end: ' + receive_string
#
#                     receiveDict = jsonpickle.decode(receive_string)
#
#                     #put with blocking=True
#                     #incomingMessageQueue.put(receiveDict, True)
#                     event = receiveDict['event']
#                     event = event.upper()
#                     if event == 'EXPLORE' or event == 'START':
#                         robot.send({
#                             "event": event
#                         })
#             except bluetooth.BluetoothError:
#                 print 'connecting to android failed, retrying'
#             except ValueError as msg:
#                 print msg
#             except Exception as msg:
#                 print msg
#
# android = piBluetooth.PiBluetooth()
# androidThreadInstance = androidThread()
# androidThreadInstance.start()

#############################################################
arena = Arena(HEIGHT, WIDTH)
# robot = Robot("192.168.14.144", 8080, robot_event_handler)
robot = Robot("127.0.0.1", 8080, robot_event_handler)
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
