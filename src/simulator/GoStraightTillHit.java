package simulator;

// Deprecated

public class GoStraightTillHit extends Task {

    @Override
    public void run() {

    }

    @Override
    public void tick() {
        double front = robot.senseFront();
        if (4.5 < front % 10 && front % 10 < 5.5) {
            robot.triggerEvent(2);
        }
        if (front < 5.5) {
            robot.finishTask(RobotEvent.OBSTACLE_IN_FRONT);
            return;
        }
        robot.x += Math.cos(Math.PI * 2 * robot.d);
        robot.y += Math.sin(Math.PI * 2 * robot.d);
    }
}
