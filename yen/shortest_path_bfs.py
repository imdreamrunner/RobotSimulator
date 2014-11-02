from constants import *
from queue import Queue, Task
from algorithm import Algorithm


class Node(object):
    def __init__(self, x = 0, y = 0, d = 0):
        self.x = x
        self.y = y
        self.d = d


class ShortestPathBFS(Algorithm):

    MAXC = 1000
    W = [0, 1, 2, 1]

    def __init__(self):
        super(ShortestPathBFS, self).__init__()
        self.h = [[[self.MAXC] * 4 for j in range(WIDTH)] for i in range(HEIGHT)]

    def print_heuristic_matrix(self):
        for d in range(4):
            for i in range(HEIGHT):
                for j in range(WIDTH):
                    print "%4d" % (self.h[i][j][d]),
                print
            print

    def run(self, arena, robot, goalX, goalY, visited, challenge):
        """
            Return next action to go shortest path
        """
        self.bfs(arena, robot, goalX, goalY)
        self.swap_h()
        self.print_heuristic_matrix()

        ans = 1
        min_dis = self.MAXC
        for k in [0, 1, 3]:
            if k == 0:
                newx, newy, newd = robot.x + DX[robot.d], robot.y + DY[robot.d], robot.d
            else:
                newx, newy, newd = robot.x, robot.y, (robot.d + k) % 4
            if self.h[newx][newy][newd] + self.W[k] < min_dis:
                min_dis = self.h[newx][newy][newd] + self.W[k]
                ans = k

        if ans == GO_STRAIGHT:
            x, y, d = robot.x, robot.y, robot.d
            unit = 1
            for i in range(1, 7):
                newx, newy, newd = x + DX[d], y + DY[d], d
                if self.h[newx][newy][d] > self.h[x][y][d]:
                    break
                x, y, d = newx, newy, newd
                unit = i

            print "Go straight unit: ", unit
            return [Task(GO_STRAIGHT, unit)]
        else:
            return [Task(ans, 1)]

    def swap_h(self):
        """
            h[x][y][d] <==> h[x][y][(d+2)%4]
        """
        for x in range(HEIGHT):
            for y in range(WIDTH):
                for d in range(2):
                    tmp = self.h[x][y][d]
                    self.h[x][y][d] = self.h[x][y][(d+2) % 4]
                    self.h[x][y][(d+2) % 4] = tmp

    def bfs(self, arena, robot, goalX, goalY):
        queue = Queue()
        free = [[[True] * 4 for j in range(WIDTH)] for i in range(HEIGHT)]
        self.h = [[[self.MAXC] * 4 for j in range(WIDTH)] for i in range(HEIGHT)]

        for d in range(4):
            self.h[goalX][goalY][d] = 0
            queue.enqueue(Node(goalX, goalY, d))
            free[goalX][goalY][d] = False

        while not queue.isEmpty():
            cur = queue.dequeue()
            x, y, d = cur.x, cur.y, cur.d
            for k in [1, 3]:
                newx, newy, newd = x, y, (d + k) % 4
                if arena.is_standable(newx, newy) and free[newx][newy][newd]:
                    queue.enqueue(Node(newx, newy, newd))
                    self.h[newx][newy][newd] = self.h[x][y][d] + 1
                    free[newx][newy][newd] = False
            #k = 0?
            for i in range(1, 5):
                newx, newy, newd = x + i*DX[d], y + i*DY[d], d
                if not arena.is_standable(newx, newy):
                    break
                if free[newx][newy][newd]:
                    queue.enqueue(Node(newx, newy, newd))
                    self.h[newx][newy][newd] = self.h[x][y][d] + 1
                    free[newx][newy][newd] = False











