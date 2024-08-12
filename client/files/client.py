import socket
import threading
import json
import time

class Client():
    def __init__(self):
        self.host = 'server'
        self.port = 8020
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_id = None
        self.client_name = None
        self.client_email = None
        self.client_deck = 0
        
    def startClient(self):
        self.s.connect((self.host, self.port))
        print('Connected to server')
        
    def sendMessage(self, data):
        print(f"Sending message: {data}")
        try:
            data_str = json.dumps(data)
            self.s.send(bytes(data_str, encoding="utf-8"))
        except socket.error as e:
            print(str(e))
            self.s.close()
        
    def receiveMessage(self):
        try:
            data = self.s.recv(1024)
            data_dict = json.loads(data.decode("utf-8"))
            print(data_dict)
            return data_dict
        except socket.error as e:
            print(str(e))