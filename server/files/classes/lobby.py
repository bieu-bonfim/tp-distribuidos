class Lobby():
    def __init__(self):
        self.players = list()
        
    def start(self):
        while True:
            #handle game execution
            continue
        
    def addPlayer(self, player):
        self.players.append(player)
        
    def removePlayer(self, player):
        self.players.remove(player)
        
    def ready(self):
        if self.players.count == 3:
            return True