import json
import socket
import threading
import thread


class Robot(threading.Thread):
    def __init__(self, host, port, handler):
        super(Robot, self).__init__()
        self.daemon = True
        self.host = host
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = port
        self.handler = handler

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