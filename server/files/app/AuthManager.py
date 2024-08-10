from controller.UserController import UserController

class AuthManager:
    def __init__(self, conn):
        self.userController = UserController(conn)

    def login(self, username, password):
        result = self.userController.login(username, password)
        return {'header': 'login', 'response': {'status': 'success', 'message': 'Usuário logado com sucesso'}}

    def register(self, username, password):
        result = self.userController.register(username, password)

    def logout(self):
        result = self.userController.logout()

    def get_user(self):
        return self.userController.get_user()