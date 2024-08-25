import Pyro5.api

@Pyro5.api.expose
class GameHandler():
    def __init__(self):
        pass
    
    def bap():
        print("bap")
        
    @Pyro5.api.expose
    def receive_event(self, message):
      print("bap")
      print(f"Received event with message: {message}")