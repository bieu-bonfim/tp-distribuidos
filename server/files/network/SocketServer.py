import socket
import threading
import json
import time as t
from client import Client
from network.RequestHandler import RequestHandler

class SocketServer():
    def __init__(self, host='0.0.0.0', port=8020):
        self.socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socketServer.bind((host, port))
        self.threads = list()
        self.clients = list()
        print('Server created!')

    
    def serverStart(self):
        self.socketServer.listen()
        print('Server started!')
        while True:
            conn, addr = self.socketServer.accept()
            client = Client(conn, addr, (len(self.clients) + 1))
            self.clients.append(client)
            print(f'Connected to {addr}')
            
            client_thread = threading.Thread(target=self.handleClient, args=(client,), daemon=True)
            client_thread.start()
            self.threads.append(client_thread)
            
    def serverStop(self):
        for client in self.clients:
            client.conn.sendall(bytes(json.dumps({'header': 'Server stopped'}), encoding="utf-8"))
            client.conn.close()
        self.socketServer.close()
        print('Server stopping...')
        
                
    def broadcastMessage(self, sender, data_dict):
        try:
            for client in self.clients:
                if client.conn != sender:
                    client.conn.sendall(bytes(json.dumps(data_dict), encoding="utf-8"))
        except socket.error as e:
            print(str(e))
            
    def sendMessage(self, receiver, data_dict):
        try:
            receiver.sendall(bytes(json.dumps(data_dict), encoding="utf-8"))
        except socket.error as e:
            print(str(e))
            
    def handleClient(self, client):
        while True:
            handler = RequestHandler(client, self)
            handler.handleRequest()
            client.conn.close()
                
                # data = client.conn.recv(1024)
                # data_dict = json.loads(data.decode("utf-8"))
                # header = data_dict['header']
                # if header == 'exit':
                #     self.serverStop()
                #     break
                # #
                # manipulação dos dados com o json recebido já convertido
                #
                # header: enter_lobby <=> lobby_id : string
                # header: create_lobby <=> none
                # header: leave_lobby <=> none
                # header: buy_booster <=> none
                # header: create_deck <=> cards : list<string>
                # header: manage_deck <=> deck_id: string, cards: list<string>
                # header: select_deck <=> deck_id: string
                # header: choose_card <=> card_id: string
                # header: choose_stat <=> stat: string
                # 
                
                # self.broadcastMessage(client.conn, data_dict)
