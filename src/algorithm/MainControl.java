package algorithm;

import simulator.Arena;
import simulator.Robot;
import simulator.RobotException;

public class MainControl {
    public Arena arena;
    public Robot robot;

    public MainControl(Arena arena, Robot robot) throws RobotException {
        this.arena = arena;
        this.robot = robot;
        new RobotControl(arena, robot);
    }
}
