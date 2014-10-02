WIDTH = 20
HEIGHT = 15
MAXC = 1000000

h = [[[0 for d in range(4)] for j in range(WIDTH)] for i in range(HEIGHT)]
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]


def explore(knownWorld, x, y, d, goalX, goalY):
    global h
    h = [[[MAXC for d in range(4)] for j in range(WIDTH)] for i in range(HEIGHT)]
    update_heuristic_all(knownWorld, goalX, goalY)

    for i in range(HEIGHT):
        for j in range(WIDTH):
            print h[i][j][0],
        print
    print

    min = MAXC
    ans = 1
    for direction in range(4):
        if h[x][y][(d+direction) % 4] < min:
            min = h[x][y][(d+direction) % 4]
            ans = direction
    newx, newy, newd = x + dx[d], y + dy[d], d
    if not is_outside(newx, newy):
        if h[newx][newy][newd] < min:
            ans = 0

    return ans


def is_outside(x, y):
    return x < 0 or x >= HEIGHT or y < 0 or y >= WIDTH


def is_obstacle(knownWorld, x, y):
    if is_outside(x, y):
        return True
    return knownWorld[x][y] == 2


def update_heuristic_all(knownWorld, goalX, goalY):
    global h
    h = [[[MAXC for d in range(4)] for j in range(WIDTH)] for i in range(HEIGHT)]
    free = [[[True for d in range(4)] for j in range(WIDTH)] for i in range(HEIGHT)]

    for d in range(4):
        h[goalX][goalY][d] = 0

    while 1:
        x, y, d = -1, -1, -1
        min = MAXC
        for i in range(HEIGHT):
            for j in range(WIDTH):
                for k in range(4):
                    if free[i][j][k] and (min > h[i][j][k]):
                        x, y, d = i, j, k
                        min = h[i][j][k]
        if x == -1:
            break
        free[x][y][d] = False
        for k in range(4):
            newx, newy, newd = x, y, (d + k) % 4
            if (not is_outside(newx, newy)) and (not is_obstacle(knownWorld, newx, newy)):
                if free[newx][newy][newd] and h[newx][newy][newd] > h[x][y][d] + 1:
                    h[newx][newy][newd] = h[x][y][d] + 1
        newx, newy, newd = x + dx[d], y + dy[d], d
        if not is_outside(newx, newy) and (not is_obstacle(knownWorld, newx, newy)):
            if free[newx][newy][newd] and h[newx][newy][newd] > h[x][y][d] + 1:
                h[newx][newy][newd] = h[x][y][d] + 1


def find_path():
    pass