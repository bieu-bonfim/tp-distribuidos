import socket
import threading
import json

class Client():
    def __init__(self):
        self.host = 'server'
        self.port = 8020
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def startClient(self):
        self.s.connect((self.host, self.port))
        threading.Thread(target=self.sendMessage).start()
        threading.Thread(target=self.receiveMessage).start()
        print('Connected to server')
        
    def sendMessage(self):
        while True:
            message = input('Enter message: ')
            data = {'header': message}
            data_str = json.dumps(data)
        
            try:
                self.s.sendall(bytes(data_str, encoding="utf-8"))
            except socket.error as e:
                print(str(e))
                self.s.close()
        
    def receiveMessage(self):
        while True:
            try:
                data = self.s.recv(1024)
                data_dict = json.loads(data.decode("utf-8"))
                print(f"Received message: {data_dict['header']}")
            except socket.error as e:
                print(str(e))
                break
