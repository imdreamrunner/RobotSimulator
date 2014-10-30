import sys
from conn import Robot
from shortest_path_heuristic import shortest_path
from exploration_heuristic import explore_heuristic
from exploration_lean_wall import explore_lean_wall
from anena import Arena
from constants import *
from sensor_manager import update_known_world, print_sensors
from calibration_manager import can_calibrate_front, can_calibrate_right, can_calibrate_left
from queue import Queue, Task


visited = [[[0] * 4 for j in range(WIDTH)] for i in range(HEIGHT)]
# Initiate the goal and challenge level
goalX, goalY = 13, 18
challenge = CHALLENGE_EXPLORE_REACH_GOAL
#Count from last calibrate
go_straight_count = 0
move_count = 0
just_finish_kelly_front = False
infinite_loop = False

task_queue = Queue()


def robot_event_handler(res):
    event = res['event']
    if event == "EXPLORE":
        send_task(Task(GO_STRAIGHT, 1))
    elif event == "START":
        send_task(Task(TURN_LEFT, 1))
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
    return just_finish_kelly_front or go_straight_count >= 5 or move_count >= 7


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
    global task_queue

    if task_queue.isEmpty():
        # if task_queue empty, find next tasks need to be performed
        print "Robot position: %d %d %d " % (robot.x, robot.y, robot.d)
        sensors = res['sensors']
        print_sensors(sensors)

        # # Update map only in exploration phase
        # if challenge < CHALLENGE_RUN_REACH_GOAL:
        #     update_known_world(arena, robot, sensors)
        update_known_world(arena, robot, sensors)
        print_console()
        task_queue.enqueue_list(find_next_move())

    if not task_queue.isEmpty():
        send_task(task_queue.dequeue())


def send_task(task):
    global go_straight_count
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

    if action == GO_STRAIGHT:
        go_straight_count += quantity
    else:
        go_straight_count = 0
    send_known_world(arena)


def find_next_move():
    global goalX, goalY, challenge, just_finish_kelly_front, go_straight_count, move_count, infinite_loop
    #Check if reach goal
    if robot.x == goalX and robot.y == goalY:
        #If reach goal
        #Always kelly when reaching goal
        if not just_finish_kelly_front:
            just_finish_kelly_front = True
            return [Task(KELLY, 1)]

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
        return [Task(KELLY, 1)]
    else:
        just_finish_kelly_front = False

    #check if can calibrate_right
    if can_calibrate_right(arena, robot) and need_calibrate_left_right():
        print "calibrate right"
        move_count = 0
        return [Task(TURN_RIGHT, 1), Task(KELLY, 1), Task(TURN_LEFT, 1)]

    #check if can calibrate_left
    if can_calibrate_left(arena, robot) and need_calibrate_left_right():
        print "calibrate left"
        move_count = 0
        return [Task(TURN_LEFT, 1), Task(KELLY, 1), Task(TURN_RIGHT, 1)]

    #Use algorithm to find the appropriate action
    print "find action using algorithm"
    if challenge == CHALLENGE_RUN_REACH_GOAL:
        action = shortest_path(arena, robot, goalX, goalY, visited, challenge)
    elif challenge == CHALLENGE_EXPLORE_REACH_GOAL:
        action = explore_heuristic(arena, robot, goalX, goalY, visited, challenge)
    else:
        # check if infinite loop
        infinite_loop = infinite_loop or (visited[robot.x][robot.y][robot.d] > 2)
        if infinite_loop:
            action = explore_heuristic(arena, robot, goalX, goalY, visited, challenge)
        else:
            action = explore_lean_wall(arena, robot, goalX, goalY, visited, challenge)
    print "Action: ", action
    move_count += 1
    visited[robot.x][robot.y][robot.d] += 1
    return action


def send_known_world(arena):
    robot.send_known_world(arena, robot)
    if DISPLAY_MAP:
        mapDisplay.send_known_world(arena, robot)


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
