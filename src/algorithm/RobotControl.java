/*
 * Yen
 */

package algorithm;

import simulator.*;

import java.util.ArrayList;
import java.util.List;

import static simulator.Main.HEIGHT;
import static simulator.Main.WIDTH;

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
                        robot.doTask(new Rotate(0.25));
                    } else {

                        //wall left
                        boolean wall_head = (robot.senseFrontMid() < 10 || robot.senseFrontLeft() < 10 || robot.senseFrontRight() < 10);
                        boolean wall_right = (robot.senseRight() < 10);
                        System.out.println("wall head: " + wall_head);
                        if (!wall_head) {
                            robot.doTask(new GoStraight(10));
                        }
                        else if (!wall_right) robot.doTask(new Rotate(0.25));
                            else {

                                robot.doTask(new Rotate(0.5));
                            }

                    }
                }
            }
        };

        robot.addEventHandler(robotEventHandler);
        robot.doTask(new GoStraight(10));

    }

}
