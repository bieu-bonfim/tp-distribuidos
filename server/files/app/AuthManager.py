from controller.UserController import UserController
from datetime import datetime
class AuthManager:
    def __init__(self, conn):
        self.userController = UserController(conn)

    def login(self, username, password):
        print('Login calling database')
        result, id = self.userController.login(username, password)
        if result == False:
            return {'header': 'login', 'response': {'status': 'error', 'message': 'Usuário ou senha inválidos'}}
        return {
            'header': 'login', 
            'response': {
                'status': 'success', 
                'message': 'Usuário logado com sucesso', 
                'data': {
                    'user_id': id
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