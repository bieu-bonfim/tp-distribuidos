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
      
  def choose_deck(self, client, deck_id):
    print(f"escolhendo deck {deck_id}")
    client.set_current_deck(deck_id)

  
  
  def retrieveDeck(self, deck_id):
    print(deck_id)
    deck = self.deckController.getById(deck_id)
    if len(deck) == 0:
      return {
        'header': 'retrieve_deck',
        'response': {
          'status': 'error',
          'message': 'Deck não encontrado'
        }
      }
    else:
      cards_list = []
      print(deck)
      deck_cards = self.deckCardsController.getCardByDeck(deck[0][0])
      for card in deck_cards:
        for i in range(card[11]):
          cards_list.append(card[i])
      return {
        'header': 'retrieve_deck',
        'response': {
          'status': 'success',
          'message': 'Deck encontrado',
          'data': {
            'deck': {
              'id': deck[0][0],
              'name': deck[0][1],
              'cards': cards_list
            }
          }
        }
      }
      
