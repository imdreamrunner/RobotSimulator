from constants import *
from queue import Task
from algorithm import Algorithm


class ShortestPathHeuristic(Algorithm):

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


