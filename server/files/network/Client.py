class Client():
    def __init__(self, conn, address, player):
        self.conn = conn
        self.address = address
        self.player = player 
        self.in_lobby = False
        self.current_lobby = None
        self.username = None
        self.current_deck = 0