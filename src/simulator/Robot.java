package simulator;

import javafx.scene.layout.AnchorPane;
import javafx.scene.paint.Color;
import javafx.scene.shape.Circle;

import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.Queue;


public class Robot {
    private Arena arena;
    private Circle circle, head;
    private AnchorPane root;
    private Task task;
    private Queue<Task> taskList;
    double x, y, d;

    Robot(Arena arena) {
        this.root = arena.root;
        this.arena = arena;
        x = 95.0;
        y = 75.0;
        d = 0;
        circle = new Circle(50, Color.web("black", 0.8));
        head = new Circle(8, Color.web("white"));
        taskList = new LinkedList<Task>();
    }

    void show() {
        hide();
        display();
        root.getChildren().add(circle);
        root.getChildren().add(head);
    }

    void hide() {
        root.getChildren().remove(circle);
        root.getChildren().remove(head);
    }

    void display() {
        circle.setCenterX(5 * x);
        circle.setCenterY(5 * y);
        head.setCenterX(5 * x + 36 * Math.cos(2 * d * Math.PI));
        head.setCenterY(5 * y + 36 * Math.sin(2 * d * Math.PI));
    }

    void tick() {
        if (this.task != null) {
            task.tick();
        }
        display();
    }

    public void doTask(Task task) throws RobotException {
        if (this.task == null) {
            this.task = task;
            task.setRobot(this);
            task.run();
        } else {
            throw new RobotException(0);
        }
    }

    public void scheduleTask(Task task) throws RobotException {
        taskList.add(task);
        if (this.task == null) {
            doTask(taskList.remove());
        }
    }

    public void clearSchedule() {
        taskList.clear();
    }

    protected void finishTask(int type) {
        this.task = null;
        if (taskList.size() > 0) {
            try {
                doTask(taskList.remove());
            } catch (RobotException e) {
                e.printStackTrace();
            }
        } else {
            RobotEvent robotEvent = new RobotEvent(type);
            for (RobotEventHandler eventHandler : eventHandlers) {
                try {
                    eventHandler.onRobotEvent(robotEvent);
                } catch (RobotException e) {
                    e.printStackTrace();
                }
            }
        }
    }

    private double senseFromPoint(double x, double y, double d) {
        double distance = 0;
        while (distance < 200) {
            if (arena.hasObstacle(x + distance*Math.cos(2 * d * Math.PI), y + distance*Math.sin(2 * d * Math.PI))) {
                return distance;
            }
            distance += 0.25;
        }
        return distance;
    }

    public double senseFront() {
        double point1 = senseFromPoint(x, y, d);
        double point2 = senseFromPoint(x + 10 * Math.sin(2 * d * Math.PI),
                                       y + 10 * Math.cos(2 * d * Math.PI), d);
        double point3 = senseFromPoint(x - 10 * Math.sin(2 * d * Math.PI),
                                       y - 10 * Math.cos(2 * d * Math.PI), d);
        return Math.min(Math.min(point1, point2), point3);
    }

    public double senseLeft() {
        return senseFromPoint(x, y, d - 0.25);
    }

    public double senseRight() {
        return senseFromPoint(x, y, d + 0.25);
    }

    private List<RobotEventHandler> eventHandlers = new ArrayList<RobotEventHandler>();

    public void addEventHandler(RobotEventHandler robotEventHandler) {
        eventHandlers.add(robotEventHandler);
    }
}
