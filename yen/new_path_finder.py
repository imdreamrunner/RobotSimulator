WIDTH = 20
HEIGHT = 15
MAXC = 100

h = [[0 for j in range(WIDTH)] for i in range(HEIGHT)]
DX = [-1, 0, 1, 0]
DY = [0, 1, 0, -1]
W = [0, 1, 2, 0]


def explore(known_world, x, y, d, goalX, goalY):
    update_heuristic_all(known_world, goalX, goalY)

    for i in range(HEIGHT):
        for j in range(WIDTH):
            print "%4d" % (h[i][j]),
        print
    print

    min_dis = MAXC
    ans = 1

    for k in range(4):
        newx, newy, newd = x+DX[(d+k) % 4], y+DY[(d+k) % 4], (d+k) % 4
        if k != 0 or is_standable(known_world, newx, newy):
            if not is_obstacle(known_world, newx, newy):
                if h[newx][newy] + W[k] < min_dis:
                    min_dis = h[newx][newy] + W[k]
                    ans = k
    return ans


def is_outside(x, y):
    return x < 0 or x >= HEIGHT or y < 0 or y >= WIDTH


def is_obstacle(known_world, x, y):
    if is_outside(x, y):
        return True
    return known_world[x][y] == 2


def is_free(known_world, x, y):
    if is_outside(x, y):
        return False
    return known_world[x][y] == 1


def is_standable(known_world, x, y):
    for i in range(3):
        for j in range(3):
            if not is_free(known_world, x+i-1, y+j-1):
                return False
    return True


def can_go(known_world, x, y):
    for i in range(3):
        for j in range(3):
            if is_obstacle(known_world, x+i-1, y+j-1):
                return False
    return True


def update_heuristic_all(known_world, goalX, goalY):
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
            if can_go(known_world, newx, newy):
                if free[newx][newy] and h[newx][newy] > h[x][y] + 1:
                    h[newx][newy] = h[x][y] + 1


def find_path():
    pass