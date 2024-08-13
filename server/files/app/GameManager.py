from controller.UserController import UserController
from controller.MatchController import MatchController
from random import randint
import threading

class GameManager:
    def __init__(self, lobby, conn):
        self.conn = conn
        self.cursor = conn.cursor()
        self.lobby = lobby
        self.round = 1
        self.round_attribute = ''
        self.round_cards = [None, None, None]
        self.current_player = 0
        self.matchController = MatchController(conn)
        
    def playCard(self, player, card):
        if self.round_attribute == '':
            return {
                'header': 'played_card',
                'response': {
                    'status': 'error',
                    'message': 'Atributo aind não escolhido'
                }
            }
        for i in range(len(self.lobby.players)):
            if self.lobby.players[i].username == player.username:
                self.round_cards[i] = card
        if self.round_cards.count(None) == 0:
            return {
                'header': 'played_card',
                'response': {
                    'status': 'turn_over',
                    'message': 'Cartas escolhidas',
                    'data': {
                        'player': player.username,
                        'card': card
                    }
                }
            }
        return {
            'header': 'played_card',
            'response': {
                'status': 'success',
                'message': 'Atributo não escolhido',
                'data': {
                    'player': player.username,
                    'card': card
                }
            }
        }
        
    def turnOver(self):
        return {
            'header': 'turn_over',
            'response': {
                'status': 'success',
                'message': 'Cartas reveladas!'
            }
        }
    
        
    def setAttribute(self, player, stat):
        if player.username != self.lobby.players[self.current_player].username:
            return {
                'header': 'choose_stat',
                'response': {
                    'status': 'error',
                    'message': 'Não é a sua vez de escolher o atributo'
                }
            }
        self.round_attribute = stat
        return {
            'header': 'choose_stat',
            'response': {
                'status': 'success',
                'message': f'O atributo escolhido foi {stat}',
                'data': {
                    'stat': stat
                }
            }
        }
                

    def resolveRound(self):
        arrayWinners = []
        contagem = {1: 0, 2: 0, 3: 0}
        for i in range(1,8):
            arrayWinners[i] = self.matchController.RoundResult(self.round_cards, self.round_attribute)[0]

        for player in arrayWinners:
            if player in contagem:
                contagem[player] += 1

            winner = max(contagem, key=contagem.get)
        return {
            'header': 'resolve_round',
            'response': {
                'winner': winner
            }
        }
    

    # def resolveRound(self):
    #     for i in range(len(self.lobby.players)):
    #         card = self.lobby.players[i].deck[self.round_cards[i]]
    #         if card[self.round_attribute] > max_value:
    #             max_value = card[self.round_attribute]
    #             winner = self.lobby.players[i].username
    #     self.current_player = self.lobby.players.index(winner)
    #     return {
    #         'header': 'resolve_round',
    #         'response': {
    #             'winner': winner
    #         }
    #     # }