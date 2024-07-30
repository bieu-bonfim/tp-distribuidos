from lobby import Lobby
import threading

class GameManager():
    def __init__(self):
        self.lobbies = list()
    
    def createLobby(self, lobby : Lobby):
        self.lobbies.append(lobby)
    
    def deleteLobby(self, lobby : Lobby):
        self.lobbies.remove(lobby)
    
    def startGame(self, lobby : Lobby):
        if lobby.ready():
            threading.Thread(target=lobby.start).start()