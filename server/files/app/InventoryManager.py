from controller.UserCardsController import UserCardsController
from controller.DeckController import DeckController
from controller.DeckCardsController import DeckCardsController
from controller.UserController import UserController

class InventoryManager:
  def __init__(self, conn):
    self.conn = conn
    self.userCardsController = UserCardsController(conn)
    self.deckController = DeckController(conn)
    self.deckCardsController = DeckCardsController(conn)
    self.userController = UserController(conn)
    
  def showUserInventory(self, user_id):
    all_cards = self.userCardsController.getCardNameByUser(user_id)
    card_obj = [card[0] for card in all_cards]
    all_decks = self.deckController.getDeckByUser(user_id)
    decks_obj = []
    deck_card_obj = []
    for deck in all_decks:
      deck_cards = self.deckCardsController.getCardByDeck(deck[0])
      for card in deck_cards:
        for i in range(card[11]):
          deck_card_obj.append(card[1])
      decks_obj.append({"deck_id": deck[0], "cards": deck_card_obj})
      deck_card_obj = []
    
    return {
      'header': 'show_user_inventory',
      'response': {
        'status': 'success',
        'message': 'Cartas do usuário',
        'data': {
          'cards': card_obj,
          'decks': decks_obj
        }
      }
    }
    
  def addCardToInventory(self, user_id, card_id):
    if self.userCardsController.insert((user_id, card_id, 1)):
      return {
        'header': 'add_card_to_inventory',
        'response': {
          'status': 'success',
          'message': 'Carta adicionada ao inventário do usuário'
        }
      }
    else:
      return {
        'header': 'add_card_to_inventory',
        'response': {
          'status': 'error',
          'message': 'Erro ao adicionar carta ao inventário do usuário'
        }
      }
      
  def buyBooster(self, user):
    moedas = self.userController.getCredit(user.id)
    if moedas < 10:
      return {
        'header': 'buy_booster',
        'response': {
          'status': 'error',
          'message': 'Créditos insuficientes'
        }
      }
    self.userController.updateCredit(user.id, moedas-10)
    new_cards = self.userCardsController.buyBooster(user.id)
    return {
      'header': 'buy_booster',
      'response': {
        'status': 'success',
        'message': 'Booster comprado com sucesso',
        'cards': new_cards
      }
    }
    
  def getMoedas(self, user):
    moedas = self.userController.getCredit(user.id)
    return {
      'header': 'get_moedas',
      'response': {
        'status': 'success',
        'message': 'Moedas do usuário',
        'moedas': moedas
      }
    }