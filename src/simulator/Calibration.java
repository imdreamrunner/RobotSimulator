package simulator;

public class Calibration extends Task {
    private int count;

    @Override
    public void run() {
        robot.setColor("red");
        count = 0;
    }

    @Override
    public void tick() {
        count ++;
        if (count > 15) {
            robot.setColor("black");
            robot.finishTask(RobotEvent.TASK_FINISH);
        }
    }
}
