import socket
import threading
import json
import time as t

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
                
                if client['connection'] != sender:
                    client['connection'].sendall(bytes(json.dumps(data_dict), encoding="utf-8"))
        except socket.error as e:
            print(str(e))
            
    def handleClient(self, client_socket):
        while True:
            try:
                data = client_socket.recv(1024)
                data_dict = json.loads(data.decode("utf-8"))
                if 'message' in data_dict:
                    if data_dict['message'] == 'exit':
                        self.serverStop()
                        break
                #
                # manipulação dos dados com o json recebido já convertido
                #
                self.broadcastMessage(client_socket, data_dict)
            except socket.error as e:
                print(str(e))
                break

    def serverStart(self):
        self.s.listen()
        while True:
            conn, addr = self.s.accept()
            self.clients.append({
                'connection': conn,
                'address': addr,
                # id do usuario
                'id': len(self.clients) + 1
            })
            print(f'Connected to {addr}')
            threading.Thread(target=self.handleClient, args=(conn,), daemon=True).start()
            
    def serverStop(self):
        for client in self.clients:
            client['connection'].sendall(bytes(json.dumps({'message': 'Server stopped'}), encoding="utf-8"))
            client['connection'].close()
        self.s.close()
        print('Server stopped')