from constants import *
MAXC = 1000

h = [[0 for j in range(WIDTH)] for i in range(HEIGHT)]
W = [0, 1, 2, 0]


def print_heuristic_matrix():
    for i in range(HEIGHT):
        for j in range(WIDTH):
            print "%4d" % (h[i][j]),
        print
    print


def shortest_path(arena, robot, goalX, goalY, visited, challenge):
    update_heuristic_all(arena, goalX, goalY)

    min_dis = MAXC
    ans = 1

    for k in range(4):
        newx, newy, newd = robot.x+DX[(robot.d+k) % 4], robot.y+DY[(robot.d+k) % 4], (robot.d+k) % 4
        if arena.is_standable(newx, newy):
            if (visited[newx][newy][newd] < 3) and (h[newx][newy] + W[k] < min_dis):
                min_dis = h[newx][newy] + W[k]
                ans = k

    if ans == GO_STRAIGHT:
        x, y, d = robot.x, robot.y, robot.d
        unit = 1
        for i in range(1, 6):
            newx, newy, newd = x + DX[d], y + DY[d], d
            if arena.is_outside(newx, newy) or h[newx][newy] > h[x][y]:
                break
            unit = i
            x, y, d = newx, newy, newd
        print "Go straight unit: ", unit
        return [GO_STRAIGHT, unit]

    else:
        return [ans, 1]


def update_heuristic_all(arena, goalX, goalY):

    #Use only the explored map!!!

    global h
    h = [[MAXC for j in range(WIDTH)] for i in range(HEIGHT)]
    free = [[True for j in range(WIDTH)] for i in range(HEIGHT)]

    h[goalX][goalY] = 0

    while 1:
        x, y = -1, -1
        min_dis = MAXC
        for i in range(HEIGHT):
            for j in range(WIDTH):
                if free[i][j] and (min_dis > h[i][j]):
                        x, y = i, j
                        min_dis = h[i][j]
        if x == -1:
            break
        free[x][y] = False
        for k in range(4):
            newx, newy = x+DX[k], y+DY[k]
            if arena.is_standable(newx, newy):
                if free[newx][newy] and h[newx][newy] > h[x][y] + 1:
                    h[newx][newy] = h[x][y] + 1


def find_path():
    pass