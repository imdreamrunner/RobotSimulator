/*
 * Xinzi
 */

package algorithm;

import simulator.*;

import java.util.ArrayList;
import java.util.List;

import static simulator.Main.HEIGHT;
import static simulator.Main.WIDTH;

public class AnotherControl {

    private class Point {
        public int x, y;
        public Point(int x, int y) {
            this.x = x;
            this.y = y;
        }

        public Point clone() {
            return new Point(x, y);
        }

        @Override
        public boolean equals(Object o) {
            Point p = (Point)o;
            return p.x == x && p.y == y;
        }
    }

    private class DirectionList {
        private int[] directions = new int[4];
        public void add(int d) {
            if (directions[d] != 2) {
                directions[d] = 1;
            }
        }
        public void remove(int d) {
            directions[d] = 2;
        }
        public boolean contains(int d) {
            return directions[d] == 1;
        }
    }

    Robot robot;
    Arena arena;
    RobotEventHandler robotEventHandler;
    int[][] theWorldIKnow; // 0 unknown, 1 free, 2 obstacle.
    int direction;
    Point location;
    List<Point> path;
    DirectionList[][] options;
    boolean firstMove, hasMoved = false;


    public AnotherControl(final Arena arena, final Robot robot) throws RobotException {
        this.arena = arena;
        this.robot = robot;

        theWorldIKnow = new int[HEIGHT][WIDTH];
        location = new Point(9, 7);

        path = new ArrayList<Point>();
        options = new DirectionList[HEIGHT][WIDTH];
        for (int i = 0; i < HEIGHT; i++) {
            for (int j = 0; j < WIDTH; j++) {
                options[i][j] = new DirectionList();
            }
        }

        for (int i = 6; i < 9; i++) {
            for (int j = 8; j < 11; j++) {
                theWorldIKnow[i][j] = 1; // The green area is free.
                arena.markObserved(j, i, 1);
            }
        }

        direction = 0;

        this.robotEventHandler = new RobotEventHandler() {
            @Override
            public void onRobotEvent(RobotEvent event) throws RobotException {
                markGridAsFree(location.x, location.y);
                if (event.getType() == RobotEvent.TASK_FINISH) {
                    System.out.println("Now at " + location.x + " " + location.y);
                    if (location.x == WIDTH - 2 && location.y == HEIGHT - 2) {
                        System.out.println("GOAL REACHED!");
                    }
                    if (hasMoved) {
                        if (firstMove) {
                            firstMove = false;
                        } else {
                            // mark some map here.
                        }
                    }
                    if (robot.senseFront() > 10) {
                        options[location.y][location.x].add(direction);
                    } else {
                        if (robot.senseFrontLeft() < 10) {
                            Point front = frontBlock(location.clone(), 2);
                            leftBlock(front, 1);
                            arena.markObserved(front.x, front.y, 2);
                        }
                        if (robot.senseFrontRight() < 10) {
                            Point front = frontBlock(location.clone(), 2);
                            rightBlock(front, 1);
                            arena.markObserved(front.x, front.y, 2);
                        }
                        if (robot.senseFrontMid() < 10) {
                            Point front = frontBlock(location.clone(), 2);
                            arena.markObserved(front.x, front.y, 2);
                        }
                    }
                    if (robot.senseLeft() > 10) {
                        options[location.y][location.x].add(left(direction));
                    } else {
                        Point side = leftBlock(location.clone(), 2);
                        arena.markObserved(side.x, side.y, 2);
                    }
                    if (robot.senseRight() > 10) {
                        options[location.y][location.x].add(right(direction));
                    } else {
                        Point side = rightBlock(location.clone(), 2);
                        arena.markObserved(side.x, side.y, 2);
                    }
                    if (options[location.y][location.x].contains(direction)) {
                        options[location.y][location.x].remove(direction);
                        boolean nextIsStart = false;
                        if (location.x == 3 && (location.y == 1 || location.y == 2) && direction == 2) {
                            nextIsStart = true;
                        }
                        if ((location.x == 1 || location.x == 2) && location.y == 3 && direction == 3) {
                            nextIsStart = true;
                        }
                        if (!nextIsStart && robot.senseFront() > 10) {
                            goStraight(1);
                            return;
                        }
                    }
                    if (options[location.y][location.x].contains(left(direction))){
                        turnLeft();
                        return;
                    }
                    if (options[location.y][location.x].contains(right(direction))){
                        turnRight();
                        return;
                    }
                    if(options[location.y][location.x].contains(back(direction))) {
                        turnLeft();
                        return;
                    }

                    // back track
                    if (path.size() <= 2) {
                        System.out.println("Done");
                        return;
                    }
                    path.remove(path.size() - 1);
                    Point backTo = path.get(path.size() - 1);
                    System.out.println("back track to " + backTo.x + " " + backTo.y);
                    int newDirection;
                    if (backTo.x == location.x - 1) {
                        newDirection = 2;
                    } else if (backTo.x == location.x + 1) {
                        newDirection = 0;
                    } else if (backTo.y == location.y - 1) {
                        newDirection = 3;
                    } else /* if (backTo.y == location.y - 1) */ {
                        newDirection = 1;
                    }
                    robot.scheduleTask(new Rotate(0.25*(newDirection - direction)));
                    direction = newDirection;
                    robot.scheduleTask(new GoStraight(10));
                    location.x = backTo.x;
                    location.y = backTo.y;

                }
            }
        };
        robot.addEventHandler(robotEventHandler);

        path.add(location.clone());
        turnLeft();
    }

    private void goStraight(int grid) throws RobotException {
        switch (direction) {
            case 0:
                location.x += grid;
                break;
            case 1:
                location.y += grid;
                break;
            case 2:
                location.x -= grid;
                break;
            case 3:
                location.y -= grid;
                break;
        }
        hasMoved = true;
        path.add(location.clone());
        robot.doTask(new GoStraight(10 * grid));
    }

    private void turnLeft() throws RobotException {
        direction = left(direction);
        robot.doTask(new Rotate(-0.25));
    }

    private void turnRight() throws RobotException {
        direction = right(direction);
        robot.doTask(new Rotate(0.25));
    }

    private void markGridAsFree(int x, int y) {
        for (int i = -1; i < 2; i++) {
            for (int j = -1; j < 2; j++) {
                if (x + i >= 0 && x + i < WIDTH
                 && y + j >= 0 && y + j < HEIGHT) {
                    theWorldIKnow[y+j][x+i] = 1;
                    arena.markObserved(x+i, y+j, 1);
                }
            }
        }
    }

    private int left(int d) {
        d += 3;
        d %= 4;
        return d;
    }

    private int right(int d) {
        d += 1;
        d %= 4;
        return d;
    }

    private int back(int d) {
        d += 2;
        d %= 4;
        return d;
    }

    private Point frontBlock(Point p, int grid) {
        switch (direction) {
            case 0:
                p.x += grid;
                break;
            case 1:
                p.y += grid;
                break;
            case 2:
                p.x -= grid;
                break;
            case 3:
                p.y -= grid;
                break;
        }
        return p;
    }

    private Point leftBlock(Point p, int grid) {
        switch (direction) {
            case 0:
                p.y -= grid;
                break;
            case 1:
                p.x += grid;
                break;
            case 2:
                p.y += grid;
                break;
            case 3:
                p.x -= grid;
                break;
        }
        return p;
    }
    private Point rightBlock(Point p, int grid) {
        switch (direction) {
            case 0:
                p.y += grid;
                break;
            case 1:
                p.x -= grid;
                break;
            case 2:
                p.y -= grid;
                break;
            case 3:
                p.x += grid;
                break;
        }
        return p;
    }
}
