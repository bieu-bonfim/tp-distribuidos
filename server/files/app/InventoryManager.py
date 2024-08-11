from controller.UserCardsController import UserCardsController
from controller.DeckController import DeckController

class InventoryManager:
  def __init__(self, conn):
    self.conn = conn
    self.userCardsController = UserCardsController(conn)
    self.deckController = DeckController(conn)
    
  def showUserInventory(self, user_id):
    all_cards = self.userCardsController.getCardByUser(user_id)
    card_obj = [{"card_name": card[0]} for card in all_cards]
    all_decks = self.deckController.getDeckByUser(user_id)
    decks_obj = []
    
    return {
      'header': 'show_user_inventory',
      'response': {
        'status': 'success',
        'message': 'Cartas do usuário',
        'data': {
          'cards': card_obj,
          'decks': []
        }
      }
    }