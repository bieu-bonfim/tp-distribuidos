from controller.LobbyController import LobbyController

class LobbyManager:
    def __init__(self):
        self.lobbyController = LobbyController()
        
    def createLobbyOnly(self):
        lobby = self.lobbyController.createLobbyOnly()
        return {
            'header': 'lobby_created',
            'response': {
                'status': 'success',
                'message': 'Sala criada com sucesso',
                'data': {
                    'lobby': {
                        'index': lobby.index,
                        'name': lobby.name,
                        'players_count': len(lobby.players),
                        'status': lobby.status,
                        'players': [player.username for player in lobby.players]
                    }
                }
            }
        }
        
    def createLobby(self, client):
        lobby = self.lobbyController.createLobby(client)
        client.set_in_lobby(True)
        client.set_current_lobby(lobby.index)
        return {
            'header': 'lobby_created', 
            'response': {
                'status': 'success',
                'message': 'Sala criada com sucesso',
                'data': {
                    'lobby': {
                        'index': lobby.index,
                        'name': lobby.name,
                        'players_count': len(lobby.players),
                        'status': lobby.status,
                        'players': [player.username for player in lobby.players]
                    } 
                }
            }
        }
        
        
    def getAvailableLobbies(self):
        available_lobbies = self.lobbyController.getAvailableLobbies()
        return {
            'header': 'available_lobbies',
            'response': {
                'status': 'success',
                'message': 'Salas disponíveis',
                'data': {
                    'lobbies': available_lobbies
                }
            }
        }
        
    def joinLobby(self, client, index):
        if self.lobbyController.getLobby(index) == None:
            return {
                'header': 'join_lobby',
                'response': {
                    'status': 'error',
                    'message': 'Sala não existe',
                    'data': {
                        'lobby': {}
                    }   
                }
            }
        if len(self.lobbyController.lobbies[index].players) >= self.lobbyController.lobbies[index].max_players:
            return {
                'header': 'join_lobby',
                'response': {
                    'status': 'error',
                    'message': 'Sala cheia',
                    'data': {
                        'lobby': {}
                    }
                }
            }
        if self.lobbyController.lobbies[index].status == 'playing':
            return {
                'header': 'join_lobby',
                'response': {
                    'status': 'error',
                    'message': 'Sala em jogo',
                    'data': {
                        'lobby': {}
                    }
                }
            }
        if client.get_current_lobby() == index:
            return {
                'header': 'join_lobby',
                'response': {
                    'status': 'error',
                    'message': 'Já está na sala',
                    'data': {
                        'lobby': {}
                    }
                }
            }
        if client.get_in_lobby() == True:
            return {
                'header': 'join_lobby',
                'response': {
                    'status': 'error',
                    'message': 'Já está em outra sala',
                    'data': {
                        'lobby': {}
                    }
                }
            }
        lobby = self.lobbyController.addPlayer(int(index), client.get_username())
        client.set_in_lobby(True)
        client.set_current_lobby(index)
        return {
            'header': 'join_lobby',
            'response': {
                'status': 'success',
                'message': 'Entrou na sala com sucesso',
                'data': {
                    'lobby': {
                        'index': lobby.index,
                        'name': lobby.name,
                        'player_count': len(lobby.players),
                        'status': lobby.status,
                        'players': [player.username for player in lobby.players]
                    }
                }
            }
        }
        
    def leaveLobby(self, client):
        if client.in_lobby == False:
            return {
                'header': 'leave_lobby',
                'response': {
                    'status': 'error',
                    'message': 'Não está em nenhuma sala',
                    'data': {
                        'lobby': {}
                    }
                }
            }
        lobby = self.lobbyController.removePlayer(client.current_lobby, client)
        client.in_lobby = False
        return {
            'header': 'leave_lobby',
            'response': {
                'status': 'success',
                'message': 'Saiu da sala com sucesso',
                'data': {
                    'lobby': {
                        'index': lobby.index,
                        'name': lobby.name,
                        'player_count': len(lobby.players),
                        'status': lobby.status,
                        'players': [player.username for player in lobby.players]
                    }
                }
            }
        },{
            'header': 'player_leave_lobby',
            'response': {
                'status': 'success',
                'message': 'Saiu da sala com sucesso',
                'data': {
                    'lobby': {
                        'index': lobby.index,
                        'name': lobby.name,
                        'player_count': len(lobby.players),
                        'status': lobby.status,
                        'players': [player.username for player in lobby.players]
                    }
                }
            }
        }
        
    def startGame(self, index, conn):
        if self.lobbyController.lobbies[index].status == 'playing':
            return {
                'header': 'start_game',
                'response': {
                    'status': 'error',
                    'message': 'Jogo já iniciado',
                    'data': {
                        'lobby': {}
                    }
                }
            }
        if len(self.lobbyController.lobbies[index].players) < 3:
            return {
                'header': 'start_game',
                'response': {
                    'status': 'error',
                    'message': 'Não há jogadores suficientes',
                    'data': {
                        'lobby': {}
                    }
                }
            }
        lobby = self.lobbyController.startGame(index, conn)
        return {
            'header': 'start_game',
            'response': {
                'status': 'success',
                'message': 'Jogo iniciado',
                'data': {
                    'players': [player.username for player in lobby.players]
                }
            }
        }
        
