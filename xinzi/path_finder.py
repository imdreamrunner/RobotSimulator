turn_step = 5  # One turn = walk 5 units

WIDTH = 20
HEIGHT = 15
MAX = 99999

m = []
s = []


def find_path(map, nx, ny, nd, tx, ty):
    global m, s
    m = map
    s = [[[MAX for k in range(4)] for j in range(HEIGHT)] for i in range(WIDTH)]
    update_grid(tx, ty, 0, 0)
    update_grid(tx, ty, 1, 0)
    update_grid(tx, ty, 2, 0)
    update_grid(tx, ty, 3, 0)
    straight = MAX
    if nd == 0 and nx < WIDTH - 1:
        straight = s[nx + 1][ny][nd]
    if nd == 1 and ny < HEIGHT - 1:
        straight = s[nx][ny + 1][nd]
    if nd == 2 and nx > 0:
        straight = s[nx - 1][ny][nd]
    if nd == 3 and nx > 0:
        straight = s[nx][ny - 1][nd]
    left = s[nx][ny][(nd + 3) % 4]
    right = s[nx][ny][(nd + 1) % 4]
    print "s", straight
    print "l", left
    print "r", right
    if straight <= left and straight <= right:
        return "straight"
    elif left <= straight and left <= right:
        return "left"
    else:
        return "right"


def update_grid(nx, ny, nd, val):
    if not can_go(nx, ny):  # Block by obstacle
        return MAX
    cur = s[nx][ny][nd]
    if cur <= val:
        return cur
    # print "Updating", nx, ny, nd, val
    s[nx][ny][nd] = val
    for d in range(4):
        if abs(nd - d) == 2:
            update_grid(nx, ny, d, val + turn_step * 2)
        if abs(nd - d) == 1 or abs(nd - d) == 3:
            update_grid(nx, ny, d, val + turn_step)
    if nd == 0:
        if nx > 0:
            update_grid(nx - 1, ny, nd, val + 1)
    elif nd == 1:
        if ny > 0:
            update_grid(nx, ny - 1, nd, val + 1)
    elif nd == 2:
        if nx < WIDTH - 1:
            update_grid(nx + 1, ny, nd, val + 1)
    elif nd == 3:
        if ny < HEIGHT - 1:
            update_grid(nx, ny + 1, nd, val + 1)


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