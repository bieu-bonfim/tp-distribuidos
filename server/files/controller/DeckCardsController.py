from datetime import datetime
from controller.UserCardsController import UserCardsController
from controller.CardController import CardController

class DeckCardsController:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()
        self.userCardsController = UserCardsController(conn)
        self.cardController = CardController(conn)

    def getAll(self):
        self.cursor.execute('SELECT * FROM deck_cards')
        rows = self.cursor.fetchall()
        self.conn.commit()
        return rows

    def getCardByDeck(self, deckId):
        self.cursor.execute('SELECT c.* FROM deck_cards dc INNER JOIN card c on dc.card_id = c.card_id WHERE deck_id = ?', (deckId,))
        rows = self.cursor.fetchall()
        self.conn.commit()
        return rows

    def insert(self, deck_card, userId):
        try:
            userCards = self.userCardsController.getCardIdByUser(userId)
            print("Cartas do bija: ",userCards)
            print("deck card [1]", deck_card[1])
            card = self.cardController.getById(deck_card[1])
            print ("Carta: ",card)
            if card in userCards:
                self.cursor.execute('''
                    INSERT INTO deck_cards (deck_id, card_id, quantity) VALUES (?, ?, ?)
                ''', deck_card)
                self.conn.commit()
            else: 
                print("usuario nao tem a carta")
        except Exception as e:
            print('Não foi possível inserir o deck: ',e)
            
        
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

