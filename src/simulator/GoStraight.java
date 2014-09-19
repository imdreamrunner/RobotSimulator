package simulator;

public class GoStraight extends Task {
    private double distance;
    private double passDistance;
    private double orgX, orgY, prgX, prgY;
    public GoStraight(double distance) {
        this.distance = distance;
    }
    public double getDistance() {
        return distance;
    }
    @Override
    public void run() {
        passDistance = 0;
        orgX = robot.x;
        orgY = robot.y;
        prgX = distance * Math.cos(Math.PI * 2 * robot.d);
        prgY = distance * Math.sin(Math.PI * 2 * robot.d);
        if (distance == 0) {
            robot.finishTask(RobotEvent.TASK_FINISH);
        }
    }

    @Override
    public void tick() {
        double front = robot.senseFront();
        if (4.5 < front % 10 && front % 10 < 5.5) {
            robot.triggerEvent(RobotEvent.ROBOT_IN_GRID);
        }
        passDistance += 1;
        if (passDistance > distance) {
            passDistance = distance;
        }
        robot.x = orgX + (passDistance / distance) * prgX;
        robot.y = orgY + (passDistance / distance) * prgY;
        if (passDistance == distance) {
            robot.finishTask(RobotEvent.TASK_FINISH);
        }
    }
}
