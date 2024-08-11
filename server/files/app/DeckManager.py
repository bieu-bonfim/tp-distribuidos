from controller.UserCardsController import UserCardsController
from controller.DeckController import DeckController
from controller.DeckCardsController import DeckCardsController
from controller.CardController import CardController

class DeckManager:
  def __init__(self, conn):
    self.conn = conn
    self.userCardsController = UserCardsController(conn)
    self.deckController = DeckController(conn)
    self.deckCardsController = DeckCardsController(conn)
    self.cardController = CardController(conn)

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
        card_id = self.cardController.getIdByName(card)[0]
        print(f'Card id {card_id}')
        self.deckCardsController.insert((deck_id, card_id, 1))
      return {
        'header': 'edit_deck',
        'response': {
          'status': 'success',
          'message': 'Deck editado com sucesso'
        }
      }