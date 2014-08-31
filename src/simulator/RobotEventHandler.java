package simulator;

public abstract class RobotEventHandler {
    abstract public void onRobotEvent(RobotEvent event) throws RobotException;
}
