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
        self.email = None
        self.in_lobby = False
        self.current_lobby = None
        self.current_deck = 0
        self.id = 0
        self.moeda = 0
        self.changed_stat = False
        self.stat = None
        self.played_card = [None, None, None]
        self.played_card_flag = False
        pass

    @Pyro5.api.expose
    def get_username(self):
        return self.username
    
    @Pyro5.api.expose
    def get_id(self):
        return self.id
    
    @Pyro5.api.expose
    def get_current_deck(self):
        return self.current_deck
    
    @Pyro5.api.expose
    def set_current_deck(self, deck):
        self.current_deck = deck
        
    def get_lobby(self):
        return self.current_lobby
    
    @Pyro5.api.expose
    def get_moeda(self):
        return self.moeda
    
    def set_moeda(self, moeda):
        self.moeda = moeda
        
    @Pyro5.api.expose
    def set_in_lobby(self, in_lobby):
        self.in_lobby = in_lobby
        
    @Pyro5.api.expose
    def set_current_lobby(self, lobby):
        self.current_lobby = lobby
        
    @Pyro5.api.expose
    def get_in_lobby(self):
        return self.in_lobby
    
    @Pyro5.api.expose
    def get_current_lobby(self):
        return self.current_lobby
    
    @Pyro5.api.expose
    def set_changed_stat_flag(self, flag):
        self.changed_stat = flag
        
    @Pyro5.api.expose
    def set_stat(self, stat):
        self.stat = stat
        
    @Pyro5.api.expose
    def set_played_card_flag(self, flag):
        self.played_card = flag
        
    @Pyro5.api.expose
    def set_played_card(self, card, index):
        self.played_card[index] = card