from constants import *
from queue import Task
from algorithm import Algorithm


class ShortestPathHeuristic(Algorithm):
    turn_step = 5  # One turn = walk 5 units

    MAX = 99999

    m = []
    s = []
    c = []
    task_queue = []

    arena = None

    return_task_queue = None

    def find_path_list(self, nx, ny, nd, tx, ty):
        print "tx ty", tx, ty
        self.s = [[[self.MAX for k in range(4)] for j in range(HEIGHT)] for i in range(WIDTH)]
        self.c = [[[[] for k in range(4)] for j in range(HEIGHT)] for i in range(WIDTH)]
        self.s[tx][ty][0] = 0
        self.s[tx][ty][1] = 0
        self.s[tx][ty][2] = 0
        self.s[tx][ty][3] = 0
        self.task_queue = [[tx, ty, 0], [tx, ty, 1], [tx, ty, 2], [tx, ty, 3]]
        while len(self.task_queue) > 0:
            cx, cy, cd = self.task_queue.pop()
            val = self.s[cx][cy][cd]
            for d in range(4):
                if abs(cd - d) == 1 or abs(nd - d) == 3:
                    self.update_grid(cx, cy, d, val + self.turn_step, cx, cy, cd)
            if cd == 0:
                self.update_grid(cx - 1, cy, cd, val + 1, cx, cy, cd)
            elif cd == 1:
                self.update_grid(cx, cy - 1, cd, val + 1, cx, cy, cd)
            elif cd == 2:
                self.update_grid(cx + 1, cy, cd, val + 1, cx, cy, cd)
            elif cd == 3:
                self.update_grid(cx, cy + 1, cd, val + 1, cx, cy, cd)
        path_list = []
        print self.s
        while not (nx == tx and ny == ty):
            next_step = self.c[nx][ny][nd]
            print "next step", next_step
            if next_step[2] == nd:
                inc = False
                if len(path_list) > 0:
                    last_path = path_list[-1]
                    if isinstance(last_path, int):
                        if last_path < 9:
                            path_list[-1] = last_path + 1
                            inc = True
                if not inc:
                    path_list.append(1)
            elif next_step[2] == (nd + 1) % 4:
                path_list.append("right")
            else:
                path_list.append("left")
            nx, ny, nd = next_step
            # print nx, ny, nd
        return_task_queue = []
        for task in path_list:
            if isinstance(task, int):
                return_task_queue.append(Task(GO_STRAIGHT, task))
            elif task == "right":
                return_task_queue.append(Task(TURN_RIGHT, 1))
            elif task == "left":
                return_task_queue.append(Task(TURN_LEFT, 1))
        self.return_task_queue = return_task_queue

    def update_grid(self, nx, ny, nd, val, fx, fy, fd):
        print "update", nx, ny, nd
        if not self.can_go(nx, ny):  # Block by obstacle
            print "cannot go"
            return False
        print "updated"
        cur = self.s[nx][ny][nd]
        if cur <= val:
            return False
        # print "Updating", nx, ny, nd, val
        self.s[nx][ny][nd] = val
        self.c[nx][ny][nd] = [fx, fy, fd]
        if not [nx, ny, nd] in self.task_queue:
            self.task_queue.append([nx, ny, nd])
        return True

    def can_go(self, x, y):
        return self.arena.is_standable(y, x)

    def run(self, arena, robot, goalX, goalY, visited, challenge):
        print "RUN HERE"
        self.arena = arena
        self.find_path_list(robot.y, robot.x, (robot.d+3) % 4, goalY, goalX)
        return self.return_task_queue

    """

    MAXC = 1000
    W = [0, 1, 2, 1]

    def __init__(self):
        super(ShortestPathHeuristic, self).__init__()
        self.h = [[0 for j in range(WIDTH)] for i in range(HEIGHT)]

    def print_heuristic_matrix(self):
        for i in range(HEIGHT):
            for j in range(WIDTH):
                print "%4d" % (self.h[i][j]),
            print
        print

    def run(self, arena, robot, goalX, goalY, visited, challenge):
        self.update_heuristic_all(arena, goalX, goalY)
        # print_heuristic_matrix()
        min_dis = self.MAXC
        ans = 1

        for k in [0, 1, 3]:
            newx, newy, newd = robot.x+DX[(robot.d+k) % 4], robot.y+DY[(robot.d+k) % 4], (robot.d+k) % 4
            if arena.is_standable(newx, newy):
                if (visited[newx][newy][newd] < 3) and (self.h[newx][newy] + self.W[k] < min_dis):
                    min_dis = self.h[newx][newy] + self.W[k]
                    ans = k

        if ans == GO_STRAIGHT:
            x, y, d = robot.x, robot.y, robot.d
            unit = 1
            for i in range(1, 7):
                newx, newy, newd = x + DX[d], y + DY[d], d
                if (not arena.is_standable(newx, newy)) or self.h[newx][newy] >= self.h[x][y]:
                    break
                x, y, d = newx, newy, newd
                unit = i

            print "Go straight unit: ", unit
            return [Task(GO_STRAIGHT, unit)]
        else:
            return [Task(ans, 1)]

    def update_heuristic_all(self, arena, goalX, goalY):
        self.h = [[self.MAXC for j in range(WIDTH)] for i in range(HEIGHT)]
        free = [[True for j in range(WIDTH)] for i in range(HEIGHT)]

        self.h[goalX][goalY] = 0

        while 1:
            x, y = -1, -1
            min_dis = self.MAXC
            for i in range(HEIGHT):
                for j in range(WIDTH):
                    if free[i][j] and (min_dis > self.h[i][j]):
                            x, y = i, j
                            min_dis = self.h[i][j]
            if x == -1:
                break
            free[x][y] = False
            for k in range(4):
                newx, newy = x+DX[k], y+DY[k]
                if arena.is_standable(newx, newy):
                    if free[newx][newy] and self.h[newx][newy] > self.h[x][y] + 1:
                        self.h[newx][newy] = self.h[x][y] + 1


    """