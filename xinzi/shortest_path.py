turn_step = 5  # One turn = walk 5 units

WIDTH = 20
HEIGHT = 15
MAX = 99999

m = []
s = []
c = []


def find_path_list(map, nx, ny, nd, tx, ty):
    global m, s, c
    m = map
    s = [[[MAX for k in range(4)] for j in range(HEIGHT)] for i in range(WIDTH)]
    c = [[[[] for k in range(4)] for j in range(HEIGHT)] for i in range(WIDTH)]
    update_grid(tx, ty, 0, 0, 0, 0, 0)
    update_grid(tx, ty, 1, 0, 0, 0, 0)
    update_grid(tx, ty, 2, 0, 0, 0, 0)
    update_grid(tx, ty, 3, 0, 0, 0, 0)
    path_list = []
    while not (nx == tx and ny == ty):
        next = c[nx][ny][nd]
        if next[2] == nd:
            path_list.append("straight")
        elif next[2] == (nd + 1) % 4:
            path_list.append("right")
        else:
            path_list.append("left")
        nx = next[0]
        ny = next[1]
        nd = next[2]
        # print nx, ny, nd
    return path_list


def update_grid(nx, ny, nd, val, fx, fy, fd):
    if not can_go(nx, ny):  # Block by obstacle
        return MAX
    cur = s[nx][ny][nd]
    if cur <= val:
        return cur
    # print "Updating", nx, ny, nd, val
    s[nx][ny][nd] = val
    c[nx][ny][nd] = [fx, fy, fd]
    for d in range(4):
        if abs(nd - d) == 2:
            update_grid(nx, ny, d, val + turn_step * 2, nx, ny, nd)
        if abs(nd - d) == 1 or abs(nd - d) == 3:
            update_grid(nx, ny, d, val + turn_step, nx, ny, nd)
    if nd == 0:
        if nx > 0:
            update_grid(nx - 1, ny, nd, val + 1, nx, ny, nd)
    elif nd == 1:
        if ny > 0:
            update_grid(nx, ny - 1, nd, val + 1, nx, ny, nd)
    elif nd == 2:
        if nx < WIDTH - 1:
            update_grid(nx + 1, ny, nd, val + 1, nx, ny, nd)
    elif nd == 3:
        if ny < HEIGHT - 1:
            update_grid(nx, ny + 1, nd, val + 1, nx, ny, nd)


def can_go(x, y):
    for i in range(x-1, x + 2):
        for j in range(y - 1, y + 2):
            if i < 0 or i > WIDTH - 1:
                return False
            if j < 0 or j > HEIGHT - 1:
                return False
            if m[i][j] == 2:
                return False
    return True