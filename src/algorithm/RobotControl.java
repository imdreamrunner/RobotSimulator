/*
 * Yen
 */

package algorithm;

import simulator.*;

public class RobotControl {
    Robot robot;
    Arena arena;
    RobotEventHandler robotEventHandler;


    public RobotControl(final Arena arena, final Robot robot) throws RobotException {
        this.arena = arena;
        this.robot = robot;

        this.robotEventHandler = new RobotEventHandler() {
            @Override
            public void onRobotEvent(RobotEvent event) throws RobotException {
                if (event.getType() == RobotEvent.TASK_FINISH) {
                    boolean wall_left = (robot.senseLeft() < 10);
                    if (!wall_left) {
                        robot.doTask(new Rotate(-0.25));
                        System.out.println("turn left");
                    } else {

                        //wall left
                        boolean wall_head = (robot.senseFrontMid() < 10 || robot.senseFrontLeft() < 10 || robot.senseFrontRight() < 10);
                        boolean wall_right = (robot.senseRight() < 10);
                        System.out.println("wall head: " + wall_head);
                        if (!wall_head) {
                            System.out.println("go straight");
                            robot.doTask(new GoStraight(10));
                        }
                        else if (!wall_right) {
                            robot.doTask(new Rotate(0.25));
                            System.out.println("turn right");
                        }
                            else {

                                robot.doTask(new Rotate(0.5));
                                System.out.println("turn back");
                            }

                    }
                }
            }
        };

        robot.addEventHandler(robotEventHandler);
        robot.doTask(new GoStraight(10));

    }

}
