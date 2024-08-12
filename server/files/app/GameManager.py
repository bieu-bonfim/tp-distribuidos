from controller.UserController import UserController
from random import randint

class GameManager:
    def __init__(self, lobby, conn):
        self.conn = conn
        self.cursor = conn.cursor()
        self.lobby = lobby
        self.round = 1
        self.round_attribute = ''
        self.round_cards = [3]
        self.current_player = 0
        
    def playCard(self, player, card):
        for i in range(len(self.lobby.players)):
            if self.lobby.players[i].username == player.username:
                self.round_cards[i] = card
        return {
            'header': 'play_card',
            'response': {
                'player': player.username,
                'card': card
            }
        }