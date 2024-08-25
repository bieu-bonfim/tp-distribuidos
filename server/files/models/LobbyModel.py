from app.GameManager import GameManager

class Lobby():
  def __init__(self, index, name, status):
    self.index = index
    self.name = name
    self.players = list()
    self.proxies = list()
    self.decks = list()
    self.max_players = 3
    self.status = status
    self.gameManager = None