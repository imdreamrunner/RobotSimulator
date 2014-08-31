package simulator;

public class RobotEvent {
    public static final int TASK_FINISH = 0;
    public static final int OBSTACLE_IN_FRONT = 1;
    public static final String[] message = {
            "Task finish.",
            "Obstacle in front"
    };
    private int type;
    public RobotEvent(int type) {
        this.type = type;
    }
    public int getType() {
        return type;
    }
}
