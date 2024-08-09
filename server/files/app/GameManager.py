from controller.UserController import UserController

class GameManager:
    def __init__(self, conn):
        self.userController = UserController(conn)  