import json
from app.AuthManager import AuthManager
from app.GameManager import GameManager
import time as t
import sqlite3

class RequestHandler:
    def __init__(self, client, socket_server):
        self.client = client
        self.socket_server = socket_server
        self.db_conn = sqlite3.connect('database/cryptid.db')
        self.authManager = AuthManager(self.db_conn)
        self.gameManager = GameManager(self.db_conn)

    def handleRequest(self):
        while True:
            try:    
                t.sleep(3)
                data = self.client.conn.recv(1024).decode("utf-8")
                request = json.loads(data)                
                response = self.handleRequestType(request)
                self.socket_server.sendMessage(self.client.conn, response)
            except Exception as e:
                print(str(e))
                break

    def handleRequestType(self, request):
        header = request['header']
        body = request['request']
        result = {'header': 'invalid message'}
        
        if header == 'login':
            result = self.authManager.login(body['username'], body['password'])
        elif header == 'logout':
            result = self.authManager.logout(body['username'])
        elif header == 'register':
            result = self.authManager.register(body['username'], body['password'], body['email'])
        elif header == 'play_card':
            result = self.gameManager.play_card(body['card'])
            self.socket_server.broadcastMessage(self.client.conn, body)
        
        return result