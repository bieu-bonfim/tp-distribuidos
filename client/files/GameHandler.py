import Pyro5.api

@Pyro5.api.expose
class GameHandler():
    def __init__(self, screen):
        self.screen = screen
        self.game_screen = None
    
    def bap():
        print("bap")
        
    @Pyro5.api.expose
    def receive_event(self, message):
        print("bap")
        print(f"Received event with message: {message}")

    @Pyro5.api.expose
    def update_players(self, players):
        self.screen.update_players(players)
        
    @Pyro5.api.expose
    def start_game(self, players):
        print("Starting game")
        self.screen.start_game(players)
        print("Starting game 2")
