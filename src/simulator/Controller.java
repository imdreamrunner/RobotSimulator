package simulator;

import javafx.event.ActionEvent;

public class Controller {
    private Arena arena;
    private Robot robot;

    public void setArenaAndRobot(Arena arena, Robot robot) {
        this.arena = arena;
        this.robot = robot;
    }

    public void onMoveClick(ActionEvent event) {
        // robot.setSpeed(10);
    }

    public void onStopClick(ActionEvent event) {
        // robot.setSpeed(0);
    }

    public void onLeftClick(ActionEvent event) {
        // robot.setRotate(- 0.5);
    }

    public void onRightClick(ActionEvent event) {
        // robot.setRotate(0.5);
    }

    public void onAheadClick(ActionEvent event) {
        // robot.setRotate(0);
    }
}
