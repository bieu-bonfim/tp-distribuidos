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
        self.winners = {0: 0, 1: 0, 2: 0}
        self.current_player = 0
        self.matchController = MatchController(conn)
        self.userController = UserController(conn)
        self.max_rounds = 3
        
    def playCard(self, player, card):
        print('playing card')
        if self.round_attribute == '':
            return {
                'header': 'played_card',
                'response': {
                    'status': 'error',
                    'message': 'Atributo ainda não escolhido'
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
                'message': 'Carta escolhida',
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
        str_response = f'O atributo escolhido foi {stat}'
        return {
            'header': 'choose_stat',
            'response': {
                'status': 'success',
                'message': str_response,
                'data': {
                    'stat': stat
                }
            }
        }

    def resolveRound(self):
        print("resolvendo round")
        winner = 0
        print('passo 1')
        card, winner  = self.matchController.RoundResult(self.round_cards, self.round_attribute)
        if card == 0:
            print('draw')
            result = {
                'header': 'resolve_round',
                'response': {
                    'status': 'draw',
                    'message': 'Empate! Ninguém ganhou essa rodada',
                }
            }
        else:
            print('passo 2')
            print('winner', winner)
            print('card', card)
            self.winners[winner] += 1
            result = {
                'header': 'resolve_round',
                'response': {
                    'status': 'success',
                    'message': 'Rodada resolvida, o vencedor foi ' + self.lobby.players[winner].username,
                    'winner_index': winner,
                    'winner': self.lobby.players[winner].username
                }
            }
        print('passo 3')
        print('winners', self.winners)
        self.current_player = (self.current_player + 1) % 3
        print('passo 4')
        print('current_player', self.current_player)
        print('passo 5')
        print('round', self.round)
        self.round_attribute = ''
        self.round_cards = [None, None, None]
        self.round += 1
        if self.round-1 >= self.max_rounds:
            return {
                'header': 'resolve_round',
                'response': {
                    'status': 'game_over',
                    'message': 'Rodada resolvida, o vencedor foi: ' + self.lobby.players[winner].username,
                    'winner_index': winner,
                    'winner': self.lobby.players[winner].username
                }
            }
        return result
        
    def resolveGame(self):
        winner = max(self.winners, key=self.winners.get)

        match_data = { 'winner_deck': self.lobby.players[winner].current_deck, 
                        'other_deck1': self.lobby.players[(winner+1)%3].current_deck,
                        'other_deck2': self.lobby.players[(winner+2)%3].current_deck, 
                    }
        
        match_data = [match_data['winner_deck'], match_data['other_deck1'], match_data['other_deck2']]

        print("---------- Inserindo Partida no Banco ----------")
        self.matchController.insert(tuple(match_data))
        print("---------- Inserida ----------")
        print(self.lobby.players[winner])
        self.userController.addCreditWin(self.lobby.players[winner].username)
        return {
            'header': 'resolve_game',
            'response': {
                'status': 'success',
                'message': 'Jogo encerrado, o vencedor foi ' + self.lobby.players[winner].username,
                'winner_index': winner,
                'winner': self.lobby.players[winner].username
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