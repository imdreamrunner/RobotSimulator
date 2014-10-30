from bluetooth import *
import logging
import threading

class PiBluetooth:
    def __init__(self):
        self.UUID = "a1513d56-2b38-421d-bee3-4286f12f9866"
        self.client_sock = BluetoothSocket ( RFCOMM )
        self.btAdd = "08:60:6E:A5:88:E4"
        self.mutex = threading.Lock()

    def connect(self):
        self.mutex.acquire()
        try:
            logging.debug("bluetooth finding service..")
            service_match = find_service(uuid=self.UUID, address=self.btAdd)
            while len(service_match) == 0:
                service_match = find_service(uuid=self.UUID, address=self.btAdd)
            first_match = service_match[0]
            port = first_match["port"]
            host = first_match["host"]

            self.client_sock.setblocking(True)
            self.client_sock.connect((host,port))
            self.isConnected = True

        finally:
            self.mutex.release()

    def close(self):
        self.mutex.acquire()
        try:
            self.client_sock.setblocking(True)
            self.client_sock.close()
            self.isConnected = False
            logging.info('Bluetooth disconnected')
        finally:
            self.mutex.release()

    def send(self,data):

        self.mutex.acquire()
        try:
            if self.isConnected == False:
                logging.warning('No bluetooth connection, abort sending data')
                return None

            self.client_sock.setblocking(True)
            self.client_sock.send(str(data))
            logging.info('Bluetooth sent data: '+str(data))
        finally:
            self.mutex.release()

    def receive(self):
        self.mutex.acquire()
        try:

            if self.isConnected == False:
                logging.warning('No bluetooth connection, abort sending data')
                return None
            self.client_sock.setblocking(False)

            result = ''
            data = self.client_sock.recv(1)
            result += data
            while(data!='}'):
                data = self.client_sock.recv(1)
                result += data

            logging.info('Bluetooth received data: '+result)
            return result
        except IOError:
            logging.log(5,'Bluetooth non-blocking receive')
            return ''
        finally:
            self.mutex.release()

    def connected(self):
        self.mutex.acquire()
        try:
            return self.isConnected
        finally:
            self.mutex.release()