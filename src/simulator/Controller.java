package simulator;

import javafx.event.ActionEvent;
import org.json.simple.JSONObject;

public class Controller {
    private Arena arena;
    private Robot robot;
    private AlgoConnect algoConnect;

    public void setArenaAndRobot(Arena arena, Robot robot, AlgoConnect algoConnect) {
        this.arena = arena;
        this.robot = robot;
        this.algoConnect = algoConnect;
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

    public void onExploreClick() {
        JSONObject jsonObject = new JSONObject();
        jsonObject.put("event", "EXPLORE");
        this.algoConnect.sendMessage(jsonObject.toJSONString());
    }

    public void onStartClick() {
        JSONObject jsonObject = new JSONObject();
        jsonObject.put("event", "START");
        this.algoConnect.sendMessage(jsonObject.toJSONString());
    }

    public void onReconnect() {
        Main.algo.breakLoop();
    }
}
