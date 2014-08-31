package simulator;

public class GoStraightTillHit extends Task {

    @Override
    public void run() {

    }

    @Override
    public void tick() {
        if (robot.senseFront() < 15.5) {
            robot.finishTask(RobotEvent.OBSTACLE_IN_FRONT);
            return;
        }
        robot.x += Math.cos(Math.PI * 2 * robot.d);
        robot.y += Math.sin(Math.PI * 2 * robot.d);
    }
}
