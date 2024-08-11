from controller.UserController import UserController
from random import randint

class GameManager:
    def __init__(self, conn):
        self.lobby = None
        self.round = 0
        self.current_player = randint(0, 3)