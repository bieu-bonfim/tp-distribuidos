from network.GameMembrane import GameMembrane

class Client():
    def __init__(self, conn, address, player):
        self.conn = conn
        self.address = address
        self.player = player 
        self.in_lobby = False
        self.current_lobby = None
        self.username = None
        self.current_deck = 0
        self.id = None
        
    def __init__(self, lobbyManager, db_conn, username, password):
        self.conn = None
        self.address = None
        self.in_lobby = False
        self.current_lobby = None
        self.username = username
        self.current_deck = 0
        self.gameMembrane = GameMembrane(self, lobbyManager, db_conn)
        self.id = self.gameMembrane.login(username, password)