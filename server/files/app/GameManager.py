from controller.UserController import UserController
from random import randint
import threading

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
        if self.round_cards.count(3) == 0:
            pass
            
        return {
            'header': 'play_card',
            'response': {
                'player': player.username,
                'card': card
            }
        }
        
    def setAttribute(self, player, attribute):
        if player.username != self.lobby.players[self.current_player].username:
            return {
                'header': 'set_attribute',
                'response': {
                    'status': 'error',
                    'message': 'Não é a sua vez'
                }
            }
        self.round_attribute = attribute
        return {
            'header': 'set_attribute',
            'response': {
                'attribute': attribute
            }
        }
        
    def resolveRound(self):
        max_value = 0
        winner = ''
        for i in range(len(self.lobby.players)):
            card = self.lobby.players[i].deck[self.round_cards[i]]
            if card[self.round_attribute] > max_value:
                max_value = card[self.round_attribute]
                winner = self.lobby.players[i].username
        self.current_player = self.lobby.players.index(winner)
        return {
            'header': 'resolve_round',
            'response': {
                'winner': winner
            }
        }