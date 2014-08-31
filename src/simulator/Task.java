package simulator;

public abstract class Task {
    protected Robot robot;
    abstract public void run();
    abstract public void tick();
    public void setRobot(Robot robot) {
        this.robot = robot;
    }
}
