package simulator;

import algorithm.MainControl;
import javafx.application.Application;
import javafx.application.Platform;
import javafx.event.EventHandler;
import javafx.fxml.FXMLLoader;
import javafx.scene.Scene;
import javafx.scene.layout.AnchorPane;
import javafx.stage.Stage;
import javafx.stage.WindowEvent;

public class Main extends Application {

    public static int WIDTH = 20;
    public static int HEIGHT = 15;

    @Override
    public void start(Stage primaryStage) throws Exception{
        /* create stage */
        FXMLLoader fxmlLoader = new FXMLLoader();
        AnchorPane root = (AnchorPane) fxmlLoader.load(getClass().getResource("simulator.fxml").openStream());
        primaryStage.setTitle("Simulator Test");
        primaryStage.setScene(new Scene(root/*, 300, 275*/));

        /* load the arena */
        Arena arena = new Arena(root);
        arena.show();

        /* display the robot */
        Robot robot = new Robot(arena);
        robot.show();

        Controller controller = fxmlLoader.getController();
        controller.setArenaAndRobot(arena, robot);

        /* for JavaFX only */
        primaryStage.setOnCloseRequest(new EventHandler<WindowEvent>() {
            @Override
            public void handle(WindowEvent t) {
                Platform.exit();
                System.exit(0);
            }
        });

        /* display stage */
        primaryStage.show();

        Runner runner = new Runner(arena, robot);
        runner.run();

        MainControl mainControl = new MainControl(arena, robot);
    }


    public static void main(String[] args) {
        launch(args);
    }
}
