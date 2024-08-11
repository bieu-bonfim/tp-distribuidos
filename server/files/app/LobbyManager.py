from controller.LobbyController import LobbyController

class LobbyManager:
    def __init__(self):
        self.lobbyController = LobbyController()
        
    def createLobby(self, client):
        lobby = self.lobbyController.createLobby(client)
        return {
            'header': 'lobby_created', 
            'response': {
                'status': 'success',
                'message': 'Sala criada com sucesso',
                'data': {
                    'lobby': {
                        'index': lobby.index,
                        'name': lobby.name,
                        'players': len(lobby.players),
                        'status': lobby.status
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
        if client in self.lobbyController.lobbies[index].players:
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
        if client.in_lobby == True:
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
        client.in_lobby = True
        lobby = self.lobbyController.addPlayer(int(index), client)
        return {
            'header': 'join_lobby',
            'response': {
                'status': 'success',
                'message': 'Entrou na sala com sucesso',
                'data': {
                    'lobby': {
                        'index': lobby.index,
                        'name': lobby.name,
                        'players': len(lobby.players),
                        'status': lobby.status
                    }
                }
            }
        }