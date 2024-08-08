import json

class RequestHandler:
    def __init__(self, client, socket_server):
        self.client = client
        self.socket_server = socket_server

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
            return self.login(request['username'], request['password'])
        elif header == 'logout':
            return self.logout(request['username'])
        elif header == 'register':
            return self.register(request['username'], request['password'])
        elif header == 'buyBooster':
            return self.buyBooster(request['user_id'], request['booster_id'])
        elif header == 'getAvailableBoosters':
            return self.getAvailableBoosters()
        else:
            self.socket_server.broadcastMessage(self.client.conn, {'header': 'broadcasted invalid message'})
            return {'header': 'broadcasted invalid message to all other users'}
        