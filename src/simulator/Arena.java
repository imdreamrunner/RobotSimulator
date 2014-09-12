package simulator;

import javafx.application.Platform;
import javafx.scene.Group;
import javafx.scene.layout.AnchorPane;
import javafx.scene.paint.Color;
import javafx.scene.shape.Rectangle;

import java.io.File;
import java.util.Scanner;

public class Arena {
    protected AnchorPane root;
    private boolean[][] map;
    private int[][] marked;
    private Group obstacles;
    private Group observedObstacles;
    private Rectangle board, green, start, goal;

    private static Color lightGreen = Color.web("#55FF55", 0.5);
    private static Color lightRed = Color.web("#FF5555", 0.5);

    public Arena(AnchorPane root) {
        this.root = root;

        board = new Rectangle(50 * Main.WIDTH, 50 * Main.HEIGHT, Color.web("#CCCCCC"));
        green = new Rectangle(50 * 3, 50 * 3, Color.web("#00FF00"));
        start = new Rectangle(50 * 3, 50 * 3, Color.web("#CC9900"));
        goal = new Rectangle(50 * 3, 50 * 3, Color.web("#CC0099"));
        green.setX(8 * 50);
        green.setY(6 * 50);
        start.setX(0);
        start.setY(0);
        goal.setX(850);
        goal.setY(600);

        map = new boolean[Main.HEIGHT][Main.WIDTH];
        marked = new int[Main.HEIGHT][Main.WIDTH];

        obstacles = new Group();
        observedObstacles = new Group();

        try {
            Scanner scanner = new Scanner(new File("arena.txt"));
            for (int i = 0; i < Main.HEIGHT; i++) {
                if (!scanner.hasNextLine()) {
                    throw new Exception("Invalid arena file.");
                }
                String line = scanner.nextLine();
                if (line.length() != Main.WIDTH) {
                    throw new Exception("Invalid arena file.");
                }
                for (int j = 0; j < Main.WIDTH; j++) {
                    map[i][j] = line.charAt(j) == '1';
                }
            }
            scanner.close();
        } catch (Exception ex) {
            System.out.println(ex.getMessage());
            ex.printStackTrace();
        }
    }

    void tick() {
        Platform.runLater(new Runnable() {
            @Override
            public void run() {
                observedObstacles.getChildren().clear();
                for (int i = 0; i < Main.HEIGHT; i++) {
                    for (int j = 0; j < Main.WIDTH; j++) {
                        if (marked[i][j] == 1) {
                            Rectangle obstacle = new Rectangle(50, 50, lightGreen);
                            obstacle.setX(50.0 * j);
                            obstacle.setY(50.0 * i);
                            observedObstacles.getChildren().add(obstacle);
                        } else if(marked[i][j] == 2) {
                            Rectangle obstacle = new Rectangle(50, 50, lightRed);
                            obstacle.setX(50.0 * j);
                            obstacle.setY(50.0 * i);
                            observedObstacles.getChildren().add(obstacle);
                        }
                    }
                }
            }
        });
    }

    protected boolean hasObstacle(int x, int y) {
        try {
            return map[y][x];
        } catch (ArrayIndexOutOfBoundsException ex) {
            return true;
        }
    }

    protected boolean hasObstacle(double x, double y) {
        if (x <= 0 || y <= 0) return true;
        if (x > Main.WIDTH * 10 || y > Main.HEIGHT * 10) return true;
        if (hasObstacle((int)Math.floor((x + 0.1)/10), (int)Math.floor((y + 0.1)/10))) return true;
        if (hasObstacle((int)Math.floor((x - 0.1)/10), (int)Math.floor((y + 0.1)/10))) return true;
        if (hasObstacle((int)Math.floor((x + 0.1)/10), (int)Math.floor((y - 0.1)/10))) return true;
        if (hasObstacle((int)Math.floor((x - 0.1)/10), (int)Math.floor((y - 0.1)/10))) return true;
        return false;
    }

    public void show() {
        root.getChildren().add(board);
        root.getChildren().add(obstacles);
        root.getChildren().add(green);
        root.getChildren().add(start);
        root.getChildren().add(goal);
        root.getChildren().add(observedObstacles);
        obstacles.getChildren().removeAll();
        for (int i = 0; i < Main.HEIGHT; i++) {
            for (int j = 0; j < Main.WIDTH; j++) {
                if (map[i][j]) {
                    Rectangle obstacle = new Rectangle(50, 50, Color.web("blue", 0.7));
                    obstacle.setX(50.0 * j);
                    obstacle.setY(50.0 * i);
                    obstacles.getChildren().add(obstacle);
                }
            }
        }
    }

    public void hide() {
        root.getChildren().remove(board);
        root.getChildren().remove(green);
        root.getChildren().remove(start);
        root.getChildren().remove(goal);
        root.getChildren().remove(obstacles);
        root.getChildren().remove(observedObstacles);
        obstacles.getChildren().clear();
        observedObstacles.getChildren().clear();
    }

    public void markObserved(int x, int y, boolean hasObstacle) {
        try {
            marked[y][x] = hasObstacle ? 2 : 1; // free 1, not free 2.
        } catch (ArrayIndexOutOfBoundsException ex) {

        }
    }
}
