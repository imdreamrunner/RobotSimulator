/*
 * This class has been created with non profit purposes
 * in order to explain a specific technology functionality
 * usage, feel free to add/remove/update anything in this code.
 * 
 * Do
 * Epic
 * Coding
 * 
 * http://www.doepiccoding.com/blog
 */

package simulator;

import javafx.application.Platform;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.JSONValue;

import java.io.IOException;
import java.io.InputStream;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;
/**
 * @author Martin Cazares
 */

public class AlgoConnect {
    private ServerSocket serverSocket = null;
    private Thread serverSocketThread;
    private Socket socket;
    private boolean break_loop = false;

    /**
     * Method to start thread running socket functionality
     */
    public void startSocket(){
        serverSocketThread = new Thread(new Runnable() {
            @Override
            public void run() {
                System.out.println("Starting socket server...");
                setMainStageTitle("Starting socket server...");
                socket = null;
                try {
                    serverSocket = new ServerSocket(8080);
                } catch (IOException e) {
                    e.printStackTrace();
                }
                try {
                    while (true) {
                        setMainStageTitle("Waiting for connection.");
                        socket = serverSocket.accept();
                        System.out.println("Socket connected...");
                        setMainStageTitle("Socket connected.");
                        PrintWriter out = new PrintWriter(socket.getOutputStream());
                        InputStream is = socket.getInputStream();
                        break_loop = false;
                        while (!Thread.currentThread().isInterrupted() && !break_loop) {
                            int availableBytes = is.available();
                            while (availableBytes < 1 && !break_loop) {
                                try{Thread.sleep(100);}catch(InterruptedException ie){ie.printStackTrace();}
                                availableBytes = is.available();
                            }
                            if (availableBytes == 0) break;
                            byte[] buffer = new byte[availableBytes];
                            int is_result = is.read(buffer, 0, availableBytes);
                            if (is_result < 0) break;
                            String read = new String(buffer);
                            for (String line : read.split("\n")) {
                                System.out.println("Received: " + line);
                                process(line);
                            }
                        }
                        System.out.println("Socket disconnected.");
                        setMainStageTitle("Socket disconnected.");
                        is.close();
                        out.close();
                    }
                } catch (IOException e) {
                    e.printStackTrace();
                }
                if (serverSocket != null) {
                    try {
                        serverSocket.close();
                    } catch (IOException e) {e.printStackTrace();}
                }
            }
        });
        serverSocketThread.start();
    }

    /**
     * Method to stop thread running socket functionality
     */
    public void stopSocket(){
        serverSocketThread.interrupt();
        if(serverSocket != null){
            try {
                serverSocket.close();
            } catch (IOException e) {e.printStackTrace();}
        }
    }

    public void sendMessage(String message) {
        try {
            PrintWriter out = new PrintWriter(socket.getOutputStream());
            out.println(message);
            out.flush();
        } catch (Exception ex) {
            System.out.println("Connection error.");
        }
    }

    public void process(String message) {
        JSONObject jsonObject = (JSONObject) JSONValue.parse(message);
        String event = jsonObject.get("event").toString();
        // System.out.println("EVENT: " + event);
        if (event.equals("ACTION")) {
            String action = jsonObject.get("action").toString();
            try {
                if (action.equals("GO")) {
                    Integer quantity = ((Number)jsonObject.get("quantity")).intValue();
                    Main.robot.scheduleTask(new GoStraight(quantity * 10.0));
                } else if (action.equals("ROTATE")) {
                    Integer quantity = ((Number)jsonObject.get("quantity")).intValue();
                    Main.robot.scheduleTask(new Rotate(quantity * 0.25));
                } else if (action.equals("KELLY")) {
                    sendTaskFinish();
                }
            } catch (RobotException e) {
                e.printStackTrace();
            }
        } else if (event.equals("MAP")) {
            String map_info = jsonObject.get("map_info").toString();
            for (int i = 0; i < Main.WIDTH; i++) {
                for (int j = 0; j < Main.HEIGHT; j++) {
                    Main.arena.markObserved(i, j,
                            Integer.parseInt(""+map_info.charAt(Main.HEIGHT * (Main.WIDTH - i - 1) + j)));
                }
            }
        }
    }

    public void sendTaskFinish() {
        JSONObject obj = new JSONObject();
        obj.put("event","TASK_FINISH");
        JSONArray list = new JSONArray();
        list.add(Main.robot.senseFrontMid());
        list.add(Main.robot.senseFrontLeft());
        list.add(Main.robot.senseFrontRight());
        list.add(Main.robot.senseLeft());
        list.add(Main.robot.senseRight());
        obj.put("sensors", list);
        sendMessage(obj.toJSONString());
    }

    public void breakLoop() {
        break_loop = true;
    }

    private void setMainStageTitle(final String title) {
        Platform.runLater(new Runnable() {

            @Override
            public void run() {
                Main.primaryStage.setTitle(title);
            }
        });
    }

}
