from constants import *
from queue import Task
from algorithm import Algorithm


class ExplorationLeanWall(Algorithm):
    STATE_PREFER_GO = 0
    STATE_PREFER_RIGHT = 1

    def __init__(self):
        super(ExplorationLeanWall, self).__init__()
        self.state = self.STATE_PREFER_GO

    def run(self, arena, robot, goalX, goalY, visited, challenge):
        if challenge == CHALLENGE_EXPLORE_REACH_GOAL:
            if robot.d == 2:
                self.state = self.STATE_PREFER_GO

        if challenge == CHALLENGE_EXPLORE_REACH_START:
            if robot.d == 0:
                self.state = self.STATE_PREFER_GO

        if self.state == self.STATE_PREFER_GO:
            if arena.is_standable(robot.x + DX[robot.d], robot.y + DY[robot.d]):
                self.state = self.STATE_PREFER_RIGHT
                return [Task(GO_STRAIGHT, 1)]
            else:
                self.state = self.STATE_PREFER_GO
                return [Task(TURN_LEFT, 1)]
        else:
            # state = STATE_PREFER_RIGHT
            if arena.can_not_standable(robot.x + DX[right(robot.d)], robot.y + DY[right(robot.d)]):
                if arena.is_standable(robot.x + DX[robot.d], robot.y + DY[robot.d]):
                    self.state = self.STATE_PREFER_RIGHT
                    return [Task(GO_STRAIGHT, 1)]
                else:
                    self.state = self.STATE_PREFER_GO
                    return [Task(TURN_LEFT, 1)]
            else:
                self.state = self.STATE_PREFER_GO
                return [Task(TURN_RIGHT, 1)]



