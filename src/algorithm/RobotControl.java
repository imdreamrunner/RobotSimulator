/*
 * Yen
 */

package algorithm;

import simulator.*;

public class RobotControl {
    Robot robot;
    Arena arena;
    RobotEventHandler robotEventHandler;
    int[][] theWorldIKnow; // 0 unknown, 1 free, 2 obstacle.
    int robotX, robotY, direction;

    public RobotControl(final Arena arena, final Robot robot) throws RobotException {
        this.arena = arena;
        this.robot = robot;

        theWorldIKnow = new int[Main.HEIGHT][Main.WIDTH];
        robotX = 9;
        robotY = 7;

        for (int i = 6; i < 9; i++) {
            for (int j = 8; j < 11; j++) {
                theWorldIKnow[i][j] = 1; // The green area is free.
                arena.markObserved(j, i, false);
                direction = 0;
            }
        }

        this.robotEventHandler = new RobotEventHandler() {
            @Override
            public void onRobotEvent(RobotEvent event) throws RobotException {
                if (event.getType() == RobotEvent.TASK_FINISH) {
                    if (robot.senseFront() < 10) {
                        direction += 1;
                        direction %= 4;
                        robot.scheduleTask(new Rotate(0.25));
                    } else {
                        walk();
                        markThreeGridInFrontFree();
                        robot.doTask(new GoStraight(10));
                    }
                }
            }
        };
        robot.addEventHandler(robotEventHandler);

        walk();
        markThreeGridInFrontFree();
        robot.doTask(new GoStraight(10));

        /* Example of robot event and sensor.

        this.robotEventHandler = new RobotEventHandler() {
            @Override
            public void onRobotEvent(RobotEvent event) throws RobotException {
                if (event.getType() == RobotEvent.TASK_FINISH) {
                    robot.doTask(new GoStraightTillHit());
                } else if (event.getType() == RobotEvent.OBSTACLE_IN_FRONT) {
                    robot.doTask(new Rotate(0.25));
                }
            }
        };

        robot.addEventHandler(robotEventHandler);
        robot.doTask(new GoStraightTillHit());

        System.out.println(robot.senseFront());
        System.out.println(robot.senseLeft());
        System.out.println(robot.senseRight());

        */

        /* Examples of scheduling task
        robot.scheduleTask(new GoStraight(20));
        robot.scheduleTask(new Rotate(0.5));
        robot.scheduleTask(new GoStraightTillHit());
        */
    }

    private void walk() {
        switch (direction) {
            case 0:
                robotX += 1;
                break;
            case 1:
                robotY += 1;
                break;
            case 2:
                robotX -= 1;
                break;
            case 3:
                robotY -= 1;
                break;
        }
    }

    private void markThreeGridInFrontFree() {
        int x = robotX;
        int y = robotY;
        switch (direction) {
            case 0:
                x += 2;
            case 2:
                x --;
                arena.markObserved(x, y, false);
                arena.markObserved(x, y+1, false);
                arena.markObserved(x, y-1, false);
                break;
            case 1:
                y += 2;
            case 3:
                y --;
                arena.markObserved(x, y, false);
                arena.markObserved(x-1, y, false);
                arena.markObserved(x+1, y, false);
                break;
        }
    }
}
