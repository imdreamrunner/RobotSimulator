package simulator;

public class Rotate extends Task {
    private double rotate, passRotate;
    private double orgD;

    public Rotate(double rotate) {
        if (rotate >= 0.5) {
            rotate -= 1;
        }
        if (rotate <= - 0.5) {
            rotate += 1;
        }
        this.rotate = rotate;
    }

    @Override
    public void run() {
        passRotate = 0;
        orgD = robot.d;
    }

    @Override
    public void tick() {
        passRotate += rotate > 0 ? 0.02 : -0.02;
        if (rotate > 0 == passRotate > rotate) {
            passRotate = rotate;
        }
        robot.d = (orgD + passRotate) % 1;
        if (passRotate == rotate) {
            robot.finishTask(RobotEvent.TASK_FINISH);
        }
    }
}
