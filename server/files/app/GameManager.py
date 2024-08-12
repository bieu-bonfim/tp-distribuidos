from controller.UserController import UserController
from random import randint

class GameManager:
    def __init__(self, lobby, conn):
        self.conn = conn
        self.cursor = conn.cursor()
        self.lobby = lobby
        self.round = 1
        self.current_player = randint(0, 3)
        
    def playCard(self, player, card):
        return {
            'header': 'play_card',
            'response': {
                'player': player.username,
                'card': card
            }
        }