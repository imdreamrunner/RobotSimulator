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
                Main.primaryStage.setTitle("Starting socket server...");
                socket = null;
                try {
                    serverSocket = new ServerSocket(8888);
                } catch (IOException e) {
                    e.printStackTrace();
                }
                try {
                    while (true) {
                        Main.primaryStage.setTitle("Waiting for connection.");
                        socket = serverSocket.accept();
                        System.out.println("Socket connected...");
                        Main.primaryStage.setTitle("Socket connected.");
                        PrintWriter out = new PrintWriter(socket.getOutputStream());
                        InputStream is = socket.getInputStream();
                        break_loop = false;
                        while (!Thread.currentThread().isInterrupted() && !break_loop) {
                            int availableBytes = is.available();
                            int loop = 0;
                            while (availableBytes < 1 && !break_loop) {
                                try{Thread.sleep(100);}catch(InterruptedException ie){ie.printStackTrace();}
                                availableBytes = is.available();
                                loop ++;
                                // if (loop > 1000) break;
                            }
                            if (availableBytes == 0) break;
                            byte[] buffer = new byte[availableBytes];
                            int is_result = is.read(buffer, 0, availableBytes);
                            if (is_result < 0) break;
                            String read = new String(buffer);
                            for (String line : read.split("\n")) {
                                System.out.println("line:" + line);
                                process(line);
                            }
                        }
                        System.out.println("Socket disconnected.");
                        Main.primaryStage.setTitle("Socket disconnected.");
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
        System.out.println("EVENT: " + event);
        if (event.equals("ACTION")) {
            String action = jsonObject.get("action").toString();
            Double value = ((Number)jsonObject.get("value")).doubleValue();
            try {
                if (action.equals("GO")) {
                    Main.robot.scheduleTask(new GoStraight(value));
                } else if (action.equals("ROTATE")) {
                    Main.robot.scheduleTask(new Rotate(value));
                }
            } catch (RobotException e) {
                e.printStackTrace();
            }
        } else if (event.equals("MAP")) {
            // TODO
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

}
