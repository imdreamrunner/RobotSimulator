WIDTH = 20
HEIGHT = 15
MAX = 99999

m = []
s = []


def find_path(map, nx, ny, nd, tx, ty):
    global m, s
    m = map
    s = [[MAX for j in range(HEIGHT)] for i in range(WIDTH)]
    update_grid(tx, ty, 0)
    r = s[nx + 1][ny]
    l = s[nx - 1][ny]
    d = s[nx][ny + 1]
    u = s[nx][ny - 1]
    # print r, l, d, u
    m = min(r, l, d, u)
    if m == MAX:
        print "Magic happens"
        return "right"
    # straight has priority
    if nd == 0 and r == m:
        return "straight"
    if nd == 1 and d == m:
        return "straight"
    if nd == 2 and l == m:
        return "straight"
    if nd == 3 and u == m:
        return "straight"
    if nd == 1 and r == m:
        return "left"
    if nd == 2 and d == m:
        return "left"
    if nd == 3 and l == m:
        return "left"
    if nd == 0 and u == m:
        return "left"
    return "right"


def update_grid(nx, ny, val):
    if not can_go(nx, ny):  # Block by obstacle
        return MAX
    cur = s[nx][ny]
    if cur <= val:
        return cur
    # print "Updating", nx, ny, nd, val
    s[nx][ny] = val
    update_grid(nx + 1, ny, val + 1)
    update_grid(nx - 1, ny, val + 1)
    update_grid(nx, ny + 1, val + 1)
    update_grid(nx, ny - 1, val + 1)


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