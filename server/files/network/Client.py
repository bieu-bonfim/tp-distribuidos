import Pyro5.api

@Pyro5.api.expose
class Client():
    def __init__(self, conn, address, player):
        self.conn = conn
        self.address = address
        self.player = player 
        self.in_lobby = False
        self.current_lobby = None
        self.username = None
        self.current_deck = 0
        self.id = 0
        
    def __init__(self, username):
        self.username = username
        self.in_lobby = False
        self.current_lobby = None
        self.username = None
        self.current_deck = 0
        self.id = 0
        pass
    
    @Pyro5.api.expose
    def bap(self):
        print('bap')

    def get_username(self):
        return self.username
    
    def get_id(self):
        return self.id
    
    def get_current_deck(self):
        return self.current_deck
    
    def set_current_deck(self, deck):
        self.current_deck = deck
        
    def get_lobby(self):
        return self.current_lobby