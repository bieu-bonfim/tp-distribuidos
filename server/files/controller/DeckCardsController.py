from datetime import datetime
from controller.UserCardsController import UserCardsController
from controller.CardController import CardController
from controller.DeckController import DeckController

class DeckCardsController:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()
        self.userCardsController = UserCardsController(conn)
        self.deckController = DeckController(conn)
        self.cardController = CardController(conn)

    def getAll(self):
        self.cursor.execute('SELECT * FROM deck_cards')
        rows = self.cursor.fetchall()
        self.conn.commit()
        return rows

    def getCardByDeck(self, deckId):
        self.cursor.execute('SELECT c.*, dc.quantity FROM deck_cards dc INNER JOIN card c on dc.card_id = c.card_id WHERE deck_id = ?', (deckId,))
        rows = self.cursor.fetchall()
        self.conn.commit()
        return rows

    def insert(self, deck_card):
        try:
            user_id = self.deckController.getUserByDeck(deck_card[0])[0]
            print(f'User id {user_id[0]}')
            userCards = self.userCardsController.getCardIdByUser(user_id[0])
            userCards = [card[0] for card in userCards]
            print(f'User cards {userCards}')
            card = self.cardController.getById(deck_card[1])
            print(f'Card {card}')
            if card[0] in userCards:
                self.cursor.execute('''
                    INSERT INTO deck_cards (deck_id, card_id, quantity) VALUES (?, ?, ?)
                ''', deck_card)
                self.conn.commit()
            else: 
                print("usuario nao tem a carta")
        except Exception as e:
            print('Não foi possível inserir o deck: ',e)
            
    def deleteByDeck(self, deckId):
        try:
            self.cursor.execute('''
            DELETE FROM deck_cards WHERE deck_id = ?
            ''', (deckId,))
            self.conn.commit()
        except Exception as e:
            print('Não foi possível deletar as cartas do deck: ',e)
        
    def update(self, username, email, password, createAt, deletedAt):
        self.username = username
        self.email = email
        self.password = password
        self.createAt = createAt
        self.deletedAt = deletedAt
        
    def delete(self, deckId):
        currentDate = datetime.now()
        self.cursor.execute('''
        UPDATE deck
        SET deleted_at = ?
        WHERE deck_id = ?
        ''', (currentDate, deckId))
        self.conn.commit()

