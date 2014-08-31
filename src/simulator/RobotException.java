package simulator;

public class RobotException extends Exception {
    public static final int ROBOT_IS_RUNNING = 0;
    public static final String[] message = {
            "Robot is running."
    };
    private int type;
    public RobotException(int type) {
        super(message[type]);
        this.type = type;
    }
    public int getType() {
        return type;
    }
}
