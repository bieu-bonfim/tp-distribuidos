import socket
import threading
import json
import time as t
from client import Client

class Server():
    def __init__(self):
        self.clients = list()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(('0.0.0.0', 8020))
        print('Server created')
        
    def broadcastMessage(self, sender, data_dict):
        try:
            for client in self.clients:
                # temporary solution
                t.sleep(2)
                
                if client.conn != sender:
                    client.conn.sendall(bytes(json.dumps(data_dict), encoding="utf-8"))
        except socket.error as e:
            print(str(e))
            
    def handleClient(self, client):
        while True:
            try:
                data = client.conn.recv(1024)
                data_dict = json.loads(data.decode("utf-8"))
                if data_dict['header'] == 'exit':
                    self.serverStop()
                    break
                #
                # manipulação dos dados com o json recebido já convertido
                #
                # header: enter_lobby <=> lobby_id : string, owner : bool
                # header: leave_lobby <=> none
                # header: buy_booster <=> none
                # header: create_deck <=> cards : list<string>
                # header: manage_deck <=> deck_id: string, cards: list<string>
                # header: select_deck <=> deck_id: string
                # header: choose_card <=> card_id: string
                # header: choose_stat <=> stat: string
                #
                self.broadcastMessage(client.conn, data_dict)
            except socket.error as e:
                print(str(e))
                break

    def serverStart(self):
        self.s.listen()
        while True:
            conn, addr = self.s.accept()
            client = Client(conn, addr, (len(self.clients) + 1))
            self.clients.append(client)
            print(f'Connected to {addr}')
            threading.Thread(target=self.handleClient, args=(client,), daemon=True).start()
            
    def serverStop(self):
        for client in self.clients:
            client['connection'].sendall(bytes(json.dumps({'header': 'Server stopped'}), encoding="utf-8"))
            client['connection'].close()
        self.s.close()
        print('Server stopped')