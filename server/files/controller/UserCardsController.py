from datetime import datetime
import random

class UserCardsController:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()

    def getAll(self):
        self.cursor.execute('SELECT * FROM user_cards')
        rows = self.cursor.fetchall()
        self.conn.commit()
        self.conn.close()
        return rows

    def getCardByUser(self, userId):
        self.cursor.execute('SELECT c.name FROM user_cards uc INNER JOIN card c on uc.card_id = c.card_id WHERE user_id = ?', (userId,))
        rows = self.cursor.fetchall()
        self.conn.commit()
        return rows

    def buyBooster(self, userId):
        numeros = [random.randint(1, 27),random.randint(1, 27),random.randint(1, 27)]
        print("numeros: ", numeros)
        userCard1 = (userId, numeros[0], 1)
        userCard2 = (userId, numeros[1], 1)
        userCard3 = (userId, numeros[2], 1)
        self.insert(userCard1)
        self.insert(userCard2)
        self.insert(userCard3)

    def insert(self, user_card):
        try:
            self.cursor.execute('''
                INSERT INTO user_cards (user_id, card_id, quantity) VALUES (?, ?, ?)
            ''', user_card)
            self.conn.commit()
        except Exception as e:
            print('Não foi possível inserir o deck: ',e)
            