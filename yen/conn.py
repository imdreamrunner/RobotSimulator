import json
import socket
import threading
import thread
from constants import *


class Robot(threading.Thread):
    def __init__(self, host, port, handler):
        super(Robot, self).__init__()
        self.daemon = True
        self.host = host
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = port
        self.handler = handler

        self.x = 0
        self.y = 0
        # self.d = 0
        self.d = 0

    def run(self):
        try:
            self.sock.connect((self.host, self.port))
        except socket.error:
            print "Socket connection refused."
            thread.exit()
        print "Socket connected."
        self.handler({
            "event": "READY"
        })
        while 1:
            #Now receive data
            buf = self.sock.recv(4096)
            if not buf:
                break
            try:
                for line in buf.strip().split('\n'):
                    obj = json.loads(line)
                    self.handler(obj)
            except ValueError:
                print buf

    def send(self, message):
        try:
            #Set the whole string
            jsonstring = json.dumps(message)
            self.sock.sendall(jsonstring + "\n")
            print "Sent: " + jsonstring

        except socket.error:
            #Send failed
            print 'Socket connection error.'
            thread.exit()

    def close(self):
        self.sock.close()

    def update_position(self, x, y, d):
        self.x, self.y, self.d = x, y, d

    def go_straight(self, unit):
        self.x, self.y = get_grid(self.x, self.y, self.d, unit)
        self.send({
            "event": "ACTION",
            "action": "GO",
            "quantity": unit
        })

    def turn_left(self):
        self.d = left(self.d)
        self.send({
            "event": "ACTION",
            "action": "ROTATE",
            "quantity": -1
        })

    def turn_right(self):
        self.d = right(self.d)
        self.send({
            "event": "ACTION",
            "action": "ROTATE",
            "quantity": 1
        })

    def kelly(self):
        self.send({
            "event": "ACTION",
            "action": "KELLY"
        })

    def send_known_world(self, arena, robot):
        stri = ""
        for w in range(arena.width-1, -1, -1):
            for h in range(arena.height):
                stri += str(arena.map[h][w])
        map_data = {
            "event": "MAP",
            "map_info": stri,
            "location_y": arena.width - robot.y - 1,
            "location_x": robot.x,
            "direction": right(right(robot.d))
        }
        self.send(map_data)

