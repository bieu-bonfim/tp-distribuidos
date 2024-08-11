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
            print(f"Sending message: {message}")
            data = ''
            request = ''
            if message == 'login':
                user = input('Enter username: ')
                password = input('Enter password: ')
                request = {'username': user, 'password': password}
            if message == 'register':
                user = input('Enter username: ')
                email = input('Enter email: ')
                password = input('Enter password: ')
                request = {'username': user, 'email': email, 'password': password}
            if message == 'join_lobby':
                index = input('Enter index: ')
                request = {'index': index}
            if message == 'create_lobby':
                request = {}
            if message == 'available_lobbies':
                request = {}
            if message == 'start_game':
                index = input('Enter index: ')
                request = {'index': index}
            if message == 'play_card':
                index = input('Enter index: ')
                request = {'index': index}
            data = {'header': message, 'request': request}
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
                print(data_dict)

            except socket.error as e:
                print(str(e))
                break
