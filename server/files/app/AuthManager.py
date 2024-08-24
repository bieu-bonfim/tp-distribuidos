from controller.UserController import UserController
from datetime import datetime
import Pyro5.api

@Pyro5.api.expose
class AuthManager:
    def __init__(self, conn):
        self.userController = UserController(conn)

    def login(self, username, password, client):
        result, user_id, username, email, moeda = self.userController.login(username, password)
        client.id = user_id
        client.username = username
        client.email = email
        client.moeda = moeda
        if result == False:
            return {'header': 'login', 'response': {'status': 'error', 'message': 'Usuário ou senha inválidos', 'data': {}}}
        return {
            'header': 'login', 
            'response': {
                'status': 'success', 
                'message': 'Usuário logado com sucesso', 
                'data': {
                    'user_id': user_id,
                    'username': username,
                    'email': email,
                    'moeda': moeda
                    }
                }
            }

    def register(self, username, password, email):
        dataAtual = datetime.now()
        user = (username, email, password, dataAtual)
        result = self.userController.insert(user)
        if result == False:
            return {'header': 'register', 'response': {'status': 'error', 'message': 'Usuário já existente'}}
        return {
            'header': 'register', 
            'response': {
                'status': 'success', 
                'message': 'Usuário registrado com sucesso'
                }
            }        

    def logout(self):
        result = self.userController.logout()

    def get_user(self):
        return self.userController.get_user()