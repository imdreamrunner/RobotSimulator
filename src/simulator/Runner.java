package simulator;

import java.util.Timer;
import java.util.TimerTask;

public class Runner {
    private static int FRAME = 10;

    private long time;

    private Arena arena;
    private Robot robot;
    private Timer timer;

    class NextTick extends TimerTask {
        @Override
        public void run() {
            robot.tick();
            arena.tick();
            timer.schedule(new NextTick(), 1000/FRAME / Main.speed);
        }
    }

    public Runner(final Arena arena, final Robot robot) {
        this.arena = arena;
        this.robot = robot;
        timer = new Timer();
    }

    public void run() {
        time = 0;
        timer.schedule(new NextTick(), 1000/FRAME / Main.speed);
    }
}
