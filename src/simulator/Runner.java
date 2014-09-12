package simulator;

import java.util.Timer;
import java.util.TimerTask;

public class Runner {
    private static int FRAME = 10;

    private long time;

    private Arena arena;
    private Robot robot;
    private Timer timer;
    private TimerTask timerTask;

    public Runner(final Arena arena, final Robot robot) {
        this.arena = arena;
        this.robot = robot;
        timerTask = new TimerTask() {
            @Override
            public void run() {
                robot.tick();
                arena.tick();
            }
        };
        timer = new Timer();
    }

    public void run() {
        time = 0;
        timer.schedule(timerTask, 0 , 1000/FRAME / 15);
    }
}
