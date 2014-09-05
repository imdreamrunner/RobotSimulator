package algorithm;

import simulator.*;

public class RobotControl {
    Robot robot;
    Arena arena;
    RobotEventHandler robotEventHandler;
    int[][] theWorldIKnow; // 0 unknown, 1 free, 2 obstacle.
    int robotX, robotY;

    public RobotControl(Arena arena, Robot robot) throws RobotException {
        this.arena = arena;
        this.robot = robot;

        theWorldIKnow = new int[Main.HEIGHT][Main.WIDTH];
        robotX = 8;
        robotY = 10;

        for (int i = 6; i < 9; i++)
            for (int j = 8; j < 11; j++) {
                theWorldIKnow[i][j] = 1; // The green area is free.
                arena.markObserved(j, i, false);
            }


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
}
