import Pyro5.api

@Pyro5.api.expose
class GameHandler():
    def __init__(self, screen):
        self.screen = screen
    
    def bap():
        print("bap")
        
    @Pyro5.api.expose
    def receive_event(self, message):
      print("bap")
      print(f"Received event with message: {message}")
      
    @Pyro5.api.expose
    def update_players(self, players):
        self.screen.update_players(players)
        
    # oi patrick e thulio, se tiver com muita dúvida me liga no zap, vo deixar
    # meu celular no modo barulhos e de bateria cheia, se precisar