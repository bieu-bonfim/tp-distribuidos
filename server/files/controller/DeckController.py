from datetime import datetime
import sqlite3

class DeckController:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()

    def getAll(self):
        self.cursor.execute('SELECT * FROM deck')
        rows = self.cursor.fetchall()
        self.conn.commit()
        return rows
    
    def getById(self, deckId):
        self.cursor.execute('SELECT * FROM deck WHERE deck_id = ?', (deckId,))
        rows = self.cursor.fetchall()
        self.conn.commit()
        return rows

    def getAmountDeckByUser(self, userId):
        self.cursor.execute('SELECT COUNT(*) FROM deck WHERE user_id = ?', (userId,))
        rows = self.cursor.fetchall()
        self.conn.commit()
        return rows

    def getDeckByUser(self, userId):
        self.cursor.execute('SELECT deck_id FROM deck WHERE user_id = ?', (userId,))
        rows = self.cursor.fetchall()
        self.conn.commit()
        return rows
    
    def getFirstDeckByUser(self, userId):
        self.cursor.execute('SELECT deck_id FROM deck WHERE user_id = ? LIMIT 1', (userId,))
        rows = self.cursor.fetchone()
        self.conn.commit()
        return rows
    
    def getUserByDeck(self, deckId):
        self.cursor.execute('SELECT user_id FROM deck WHERE deck_id = ?', (deckId,))
        rows = self.cursor.fetchall()
        self.conn.commit()
        return rows

    def insert(self, deck):
        try:
            print(deck)
            amountDecks = self.getAmountDeckByUser(deck[2])
            amount = [quantity[0]for quantity in amountDecks][0]
            if(amount <= 3):
                print('executar inserção')
                self.cursor.execute('''
                    INSERT INTO deck (valid, name, user_id) VALUES (?, ?, ?)
                ''', deck)
                self.conn.commit()
                print("Deck inserido com sucesso!")
            else:
                print("O usuário pode ter no máximo 3 Decks")
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


