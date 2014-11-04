import os


class Arena(object):

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.map = [[0] * width for i in range(height)]
        for i in range(height):
            for j in range(width):
                if self.isGoal(i, j):
                    self.map[i][j] = 1

    def isGoal(self, x, y):
        goals = [7, 9, 1, 1, 13, 18]
        for i in range(len(goals)):
            if i % 2 == 0:
                gx = goals[i]
                gy = goals[i+1]
                if abs(gx - x) <= 1 and abs(gy - y) <= 1:
                    return True
        return False

    def is_outside(self, x, y):
        return x < 0 or x >= self.height or y < 0 or y >= self.width

    def is_obstacle(self, x, y):
        if self.is_outside(x, y):
            return True
        return self.map[x][y] == 2

    def is_free(self, x, y):
        if self.is_outside(x, y):
            return False
        return self.map[x][y] == 1

    def is_standable(self, x, y):
        for i in range(3):
            for j in range(3):
                if not self.is_free(x+i-1, y+j-1):
                    return False
        return True

    def can_not_standable(self, x, y):
        for i in range(3):
            for j in range(3):
                if self.is_obstacle(x+i-1, y+j-1):
                    return True
        return False

    def can_go(self, x, y):
        for i in range(3):
            for j in range(3):
                if self.is_obstacle(x+i-1, y+j-1):
                    return False
        return True

    def update_known_cell(self, x, y, val):

        if self.isGoal(x, y):
            return
        if self.is_outside(x, y):
            return
        self.map[x][y] = val

    def print_console(self):
        for x in range(self.height):
            for y in range(self.width):
                print "%2d" %(self.map[x][y]),
            print
        print

    def print_known_world(self):
        """
        Print the known world in hexa format
        """
        # os.system('cls')    # windows
        # os.system('clear')  # linux

        expl = 0b11
        obst = 0xF

        for w in range(self.width):
            for h in range(self.height):
                # print self.map[h][self.width - w - 1],
                expl <<= 1
                if self.map[h][w] > 0 or True:
                    expl |= 0b1
                    obst <<= 1
                    if self.map[h][w] == 2:
                        obst |= 0b1
            # print
        # print
        expl <<= 2
        expl |= 0b11

        if obst.bit_length() % 4 != 0:
            obst <<= 4 - obst.bit_length() % 4
        obst_string = format(obst, "X")[1:]

        print "Explored:", format(expl, "X")
        print "Obstacle:", obst_string
        print


