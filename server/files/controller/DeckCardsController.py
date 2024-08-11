from datetime import datetime
import sqlite3
import UserCardsController
import CardController
conn = sqlite3.connect('../database/cryptid.db')
cursor = conn.cursor()

class DeckCardsController:
    def __init__(self, deckId, cardId, quantity):
        self.deckId = deckId
        self.cardId = cardId
        self.quantity = quantity

    def getAll():
        cursor.execute('SELECT * FROM deck_cards')
        rows = cursor.fetchall()
        conn.commit()
        return rows

    def getCardByDeck(deckId):
        cursor.execute('SELECT c.* FROM deck_cards dc INNER JOIN card c on dc.card_id = c.card_id WHERE deck_id = ?', (deckId,))
        rows = cursor.fetchall()
        conn.commit()
        return rows

    def insert(deck_card, userId):
        try:
            userCards = UserCardsController.getCardByUser(userId)
            print("Cartas do bija: ",userCards)
            print("deck card [1]", deck_card[1])
            card = CardController.getById(deck_card[1])
            print ("Carta: ",card)
            if card in userCards:
                cursor.execute('''
                    INSERT INTO deck_cards (deck_id, card_id, quantity) VALUES (?, ?, ?)
                ''', deck_card)
                conn.commit()
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
        
    def delete(deckId):
        currentDate = datetime.now()
        cursor.execute('''
        UPDATE deck
        SET deleted_at = ?
        WHERE deck_id = ?
        ''', (currentDate, deckId))
        conn.commit()

