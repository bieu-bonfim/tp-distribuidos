from datetime import datetime
from controller.DeckController import DeckController
from controller.DeckCardsController import DeckCardsController
import random
class UserController:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()
        self.deckController = DeckController(conn)
    
    def getAll(self):
        self.cursor.execute('SELECT * FROM user')
        rows = self.cursor.fetchall()
        self.conn.commit()
        return rows

    def getById(self, userId):
        self.cursor.execute('SELECT * FROM user WHERE user_id = ?', (userId,))
        rows = self.cursor.fetchall()
        self.conn.commit()
        return rows

    def getIdByUsername(self, username):
        self.cursor.execute('SELECT user_id FROM user WHERE username = ?', (username,))
        rows = self.cursor.fetchone()
        self.conn.commit()
        return rows

    def getByName(self, userName):
        self.cursor.execute('SELECT * FROM user WHERE username = ?', (userName,))
        rows = self.cursor.fetchone()
        self.conn.commit()
        return rows

    def getCredit(self, userId):
        self.cursor.execute('SELECT moeda FROM user WHERE user_id = ?', (userId,))
        rows = self.cursor.fetchone()
        self.conn.commit()
        return rows[0]
    
    def getCreditByName(self, username):
        print('entrou no getCreditByName')
        self.cursor.execute('SELECT user_id, moeda FROM user WHERE username = ?', (username,))
        rows = self.cursor.fetchone()
        self.conn.commit()
        print('rows: ', rows)
        return rows
    

    def addCreditWin(self, username):
        print('entrou no addCreditWin')
        userAndCredit = self.getCreditByName(username)
        novaMoeda = userAndCredit[1] + 10
        self.updateCredit(userAndCredit[0], novaMoeda)
        self.conn.commit()

    def updateCredit(self, userId, credit):
        print('entrou no updateCredit')
        self.cursor.execute('''
        UPDATE user
        SET moeda = ?
        WHERE user_id = ?
        ''', (credit, userId))
        self.conn.commit()

    def insert(self, user):
        try:
            username = user[0]
            existsUser = self.getByName(username)
            if existsUser == None :
                self.cursor.execute('''
                    INSERT INTO user (username, email, password, moeda, create_at) VALUES (?, ?, ?, ?, ?)
                ''', user)
                userId = self.getIdByUsername(username)
                deck1 = ("Sim", "Deck 1", userId[0])
                deck2 = ("Sim", "Deck 2", userId[0])
                deck3 = ("Sim", "Deck 3", userId[0])
                self.deckController.insert(deck1)
                self.deckController.insert(deck2)
                self.deckController.insert(deck3)
                cardIdBooster = random.sample(range(1, 28), 9)
                deckId = DeckController.getFirstDeckByUser(userId)
                for cardId in cardIdBooster:
                    deckCard = (deckId, cardId, 1)
                    DeckCardsController.insert(deckCard)
                self.conn.commit()
                return True
            else:
                return False
        except Exception as e:
            print('Não foi possível inserir usuário: ',e)
            self.conn.rollback()
        
    def update(self, username, email, password, createAt, deletedAt):
        self.username = username
        self.email = email
        self.password = password
        self.createAt = createAt
        self.deletedAt = deletedAt
        
    def delete(self, userId):
        currentDate = datetime.now()
        self.cursor.execute('''
        UPDATE user
        SET deleted_at = ?
        WHERE user_id = ?
        ''', (currentDate, userId))
        self.conn.commit()

    def login(self, username, password):
        try:
            user = self.getByName(username)
            if user != None and user[3] == password:
                return True, user[0], user[1], user[2]  # user_id, username, email
            else:
                return False, 0, None, None
        except Exception as e:
            self.conn.rollback()

