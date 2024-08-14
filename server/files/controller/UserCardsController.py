from datetime import datetime
import random
from controller.CardController import CardController
import sqlite3

class UserCardsController:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()
        self.cardController = CardController(conn)
    
    def getAll(self):
        self.cursor.execute('SELECT * FROM user_cards')
        rows = self.cursor.fetchall()
        self.conn.commit()

        return rows

    def getCardNameByUser(self, userId):
        self.cursor.execute('SELECT c.name FROM user_cards uc INNER JOIN card c on uc.card_id = c.card_id WHERE user_id = ?', (userId,))
        rows = self.cursor.fetchall()
        self.conn.commit()

        return rows

    def getCardIdByUser(self, userId):
        self.cursor.execute('SELECT c.card_id FROM user_cards uc INNER JOIN card c on uc.card_id = c.card_id WHERE user_id = ?', (userId,))
        rows = self.cursor.fetchall()   
        self.conn.commit()

        return rows

    def getQuantityCardByUser(self, userId, cardId):
        self.cursor.execute('SELECT uc.quantity FROM user_cards uc WHERE user_id = ? and card_id = ?', (userId, cardId))
        rows = self.cursor.fetchall()
        self.conn.commit()
        return rows

    def buyBooster(self, userId):
        cardIdBooster = random.sample(range(1, 28), 3)
        userCardsTuple = self.getCardIdByUser(userId)
        idCardUser = [item[0] for item in userCardsTuple]
        receivedCards = list()
        for cardId in cardIdBooster:
            receivedCards.append(self.cardController.getNameById(cardId)[0])
            if cardId not in idCardUser:
                userCard = (userId, cardId, 1)
                self.insert(userCard)
                print("Carta nova inserida com sucesso, você ganhou um: ", self.cardController.getNameById(cardId))
            else:
                quantity = self.getQuantityCardByUser(userId, cardId)
                newQuantity = [q[0]for q in quantity][0] + 1
                userCard = (userId, cardId, newQuantity)
                self.updateQuantityCard(userCard)
                print("Você já possuía esta carta, agora você tem ", newQuantity," ", self.cardController.getNameById(cardId))
        return receivedCards

    def insert(self, user_card):
        try:
            self.cursor.execute('''
                INSERT INTO user_cards (user_id, card_id, quantity) VALUES (?, ?, ?)
            ''', user_card)
            self.conn.commit()
            return True
        except Exception as e:
            print('Não foi possível inserir o deck: ',e)
            return False
            
    def updateQuantityCard(self, userCard):
        try:
            self.cursor.execute('''
            UPDATE user_cards
            SET quantity = ?
            WHERE user_id = ? and card_id = ?
            ''', (userCard))
            self.conn.commit()
            return True
        except Exception as e:
            print('Não foi possível inserir o deck: ',e)
            return False

