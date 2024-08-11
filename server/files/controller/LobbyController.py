from models.LobbyModel import Lobby

class LobbyController:
    def __init__(self):
        self.lobbies = []
        self.lobby_counter = 0
    
    def createLobby(self, client):
        lobby = Lobby(self.lobby_counter, f'Lobby {self.lobby_counter}', 'waiting')
        self.lobbies.append(lobby)
        self.addPlayer(self.lobby_counter, client)
        self.lobby_counter += 1
        return self.lobbies[self.lobby_counter - 1]
    
    def addPlayer(self, index, client):
        self.lobbies[index].players.append(client)
        return self.lobbies[index]
    
    def removePlayer(self, index, client): 
        self.lobbies[index].players.remove(client)
        return self.lobbies[index]
        
    def getAvailableLobbies(self):
        available_lobbies = []
        for lobby in self.lobbies:
            if lobby.status == 'waiting':
                available_lobbies.append({
                    'index': lobby.index,
                    'name': lobby.name,
                    'players': len(lobby.players),
                    'status': lobby.status
                })
        return available_lobbies
    
    def getPlayers(self, index):
        return self.lobbies[index].players
    
    def getLobby(self, index):
        return self.lobbies[index]
