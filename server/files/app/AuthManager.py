from controller import UserController

class AuthManager:
    def __init__(self):
        self.userController = UserController()

    def login(self, username, password):
        result = self.userController.login(username, password)
        return {'header': 'login', 'result': result}

    def register(self, username, password):
        result = self.userController.register(username, password)

    def logout(self):
        result = self.userController.logout()

    def get_user(self):
        return self.userController.get_user()