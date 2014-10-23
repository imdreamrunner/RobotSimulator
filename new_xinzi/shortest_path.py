turn_step = 5  # One turn = walk 5 units

WIDTH = 20
HEIGHT = 15
MAX = 99999

m = []
s = []
c = []
queue = []


def find_path_list(mm, nx, ny, nd, tx, ty):
    global m, s, c, queue
    m = mm
    s = [[[MAX for k in range(4)] for j in range(HEIGHT)] for i in range(WIDTH)]
    c = [[[[] for k in range(4)] for j in range(HEIGHT)] for i in range(WIDTH)]
    s[tx][ty][0] = 0
    s[tx][ty][1] = 0
    s[tx][ty][2] = 0
    s[tx][ty][3] = 0
    queue = [[tx, ty, 0], [tx, ty, 1], [tx, ty, 2], [tx, ty, 3]]
    while len(queue) > 0:
        cx, cy, cd = queue.pop()
        val = s[cx][cy][cd]
        for d in range(4):
            if abs(cd - d) == 1 or abs(nd - d) == 3:
                update_grid(cx, cy, d, val + turn_step, cx, cy, cd)
        if cd == 0:
            update_grid(cx - 1, cy, cd, val + 1, cx, cy, cd)
        elif cd == 1:
            update_grid(cx, cy - 1, cd, val + 1, cx, cy, cd)
        elif cd == 2:
            update_grid(cx + 1, cy, cd, val + 1, cx, cy, cd)
        elif cd == 3:
            update_grid(cx, cy + 1, cd, val + 1, cx, cy, cd)
    path_list = []
    while not (nx == tx and ny == ty):
        next_step = c[nx][ny][nd]
        if next_step[2] == nd:
            path_list.append("straight")
        elif next_step[2] == (nd + 1) % 4:
            path_list.append("right")
        else:
            path_list.append("left")
        nx, ny, nd = next_step
        # print nx, ny, nd
    print path_list
    return path_list


def update_grid(nx, ny, nd, val, fx, fy, fd):
    global queue
    if not can_go(nx, ny):  # Block by obstacle
        return False
    cur = s[nx][ny][nd]
    if cur <= val:
        return False
    # print "Updating", nx, ny, nd, val
    s[nx][ny][nd] = val
    c[nx][ny][nd] = [fx, fy, fd]
    if not [nx, ny, nd] in queue:
        queue.append([nx, ny, nd])
    return True


def can_go(x, y):
    for i in range(x-1, x + 2):
        for j in range(y - 1, y + 2):
            if i < 0 or i > WIDTH - 1:
                return False
            if j < 0 or j > HEIGHT - 1:
                return False
            if m[i][j] != 1:
                return False
    return True