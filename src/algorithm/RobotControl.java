package algorithm;

import simulator.*;

public class RobotControl {
    Robot robot;
    RobotEventHandler robotEventHandler;

    public RobotControl(final Robot robot) throws RobotException {
        this.robot = robot;

        this.robotEventHandler = new RobotEventHandler() {
            @Override
            public void onRobotEvent(RobotEvent event) throws RobotException {
                System.out.println("Event: " + event.message[event.getType()]);
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

        /*
        robot.scheduleTask(new GoStraight(20));
        robot.scheduleTask(new Rotate(0.5));
        robot.scheduleTask(new GoStraightTillHit());
        */
    }
}
