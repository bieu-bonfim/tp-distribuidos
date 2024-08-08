import json
from app.AuthManager import AuthManager
from app.GameManager import GameManager

class RequestHandler:
    def __init__(self, client, socket_server):
        self.client = client
        self.socket_server = socket_server
        self.authManager = AuthManager()
        self.gameManager = GameManager()

    def handleRequest(self):
        while True:
            try:    
                data = self.client.conn.recv(1024).decode("utf-8")
                if not data:
                    break
                
                request = json.loads(data)
                response = self.handleRequestType(request)
                self.client.conn.sendall(bytes(json.dumps(response), encoding="utf-8"))
                
            except Exception as e:
                print(str(e))
                break

    def handleRequestType(self, request):
        header = request['header']
        
        if header == 'login':
            result = self.authManager.login(request['username'], request['password'])
        elif header == 'logout':
            result = self.authManager.logout(request['username'])
        elif header == 'register':
            result = self.authManager.register(request['username'], request['password'])
        elif header == 'play_card':
            result = self.gameManager.play_card(request['card'])
            self.socket_server.broadcastMessage(self.client.conn, request)
        else:
            self.socket_server.broadcastMessage(self.client.conn, {'header': 'broadcasted invalid message'})
            return {'header': 'broadcasted invalid message to all other users'}
        