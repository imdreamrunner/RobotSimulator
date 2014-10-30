package simulator;

import javafx.beans.value.ChangeListener;
import javafx.beans.value.ObservableValue;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.ComboBox;
import org.json.simple.JSONObject;

import java.net.URL;
import java.util.ResourceBundle;

public class Controller implements Initializable {
    private Arena arena;
    private Robot robot;
    private AlgoConnect algoConnect;

    @FXML //  fx:id="speedBox"
    private ComboBox<String> speedBox;

    @Override // This method is called by the FXMLLoader when initialization is complete
    public void initialize(URL fxmlFileLocation, ResourceBundle resources) {
        speedBox.getSelectionModel().selectedItemProperty().addListener(new ChangeListener<String>() {
            @Override public void changed(ObservableValue<? extends String> selected, String oldSpeed, String newSpeed) {
                System.out.println("SPEED CHANGE");
                System.out.println(newSpeed);
                if (newSpeed.equals("Speed 1")) {
                    Main.speed = 1;
                }
                if (newSpeed.equals("Speed 2")) {
                    Main.speed = 2;
                }
                if (newSpeed.equals("Speed 3")) {
                    Main.speed = 3;
                }
                if (newSpeed.equals("Speed 4")) {
                    Main.speed = 4;
                }
                if (newSpeed.equals("Speed 5")) {
                    Main.speed = 5;
                }
            }
        });
    }

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
        Main.robot.x = 95;
        Main.robot.y = 75;
        Main.robot.d = 0;
        for (int i = 0; i < Main.WIDTH; i++) {
            for (int j = 0; j < Main.HEIGHT; j++) {
                Main.arena.markObserved(i, j, 0);
            }
        }
        Main.algo.breakLoop();
    }

    public void setSpeed() {
        Main.speed = 1;
    }
}
