from controller.UserCardsController import UserCardsController
from controller.DeckController import DeckController
from controller.DeckCardsController import DeckCardsController

class DeckManager:
  def __init__(self, conn):
    self.conn = conn
    self.userCardsController = UserCardsController(conn)
    self.deckController = DeckController(conn)
    self.deckCardsController = DeckCardsController(conn)

  def editDeck(self, deck_id, cards):
    deck = self.deckController.getById(deck_id)
    if len(deck) == 0:
      return {
        'header': 'edit_deck',
        'response': {
          'status': 'error',
          'message': 'Deck não encontrado'
        }
      }
    else:
      print("entrou aqui")
      self.deckCardsController.deleteByDeck(deck_id)
      for card in cards:
        self.deckCardsController.insert((deck_id, card, 1))
      return {
        'header': 'edit_deck',
        'response': {
          'status': 'success',
          'message': 'Deck editado com sucesso'
        }
      }