from datetime import datetime
from controller.CardController import CardController
from controller.DeckController import DeckController
import sqlite3

class MatchController:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()
        self.cardController = CardController(conn)
        self.deckController = DeckController(conn)

    def getAll(self):
        self.cursor.execute('SELECT * FROM match')
        rows = self.cursor.fetchall()
        self.conn.commit()
        
        return rows


    def getById(self, matchId):
        self.cursor.execute('SELECT * FROM match WHERE match_id = ?', (matchId,))
        rows = self.cursor.fetchall()
        self.conn.commit()
        return rows

    def getByAmountWinsByDeck(self, deckId):
        self.cursor.execute('SELECT COUNT(*) FROM match WHERE winner_deck_id = ?', (deckId,))
        rows = self.cursor.fetchall()
        self.conn.commit()
        return rows

    def getAmountWinsByUser(self, userId):
        userDecksList = self.deckController.getDeckByUser(userId)
        userDecks = [decks[0]for decks in userDecksList]
        amount = 0
        for i in userDecks:
            amountByDeckList = self.getByAmountWinsByDeck(i)
            amountDeck = [quantity[0]for quantity in amountByDeckList][0]
            amount = amount + amountDeck
        print("Vitórias do usuario: ",amount)
        return amount

    def insert(self, match):
        try:
            self.cursor.execute('''
                INSERT INTO match (winner_deck_id, player1_deck_id, player2_deck_id) VALUES (?, ?, ?)
            ''', match)
            conn.commit()         
        except Exception as e:
            print('Não foi possível inserir a carta: ',e)
            

    type = [
        #todo
    ]



    fear = [
        "Nem assusta",
        "Espantoso",
        "Arrepiante",
        "Temível",
        "Horripilante",
        "Incompreensível"
    ]

    dangerous = [
        "Inofensivo",
        "Fique atento",
        "Periculoso",
        "Ameaçador",
        "Mortal",
        "Fuja"
    ]

    rare = [
        "Famoso",
        "Comum",
        "Pouco Falado",
        "Desconhecido",
        "Obscuro",
        "Segredo"
    ]

    def RoundResult(self, cards, attribute):
        if cards[0] == cards[1] and cards[0] == cards[2] and cards[1] == cards[2]:
            return 0,()
        elif cards[0] == cards[1]:
            result = self.cardController.getByName(cards[2])
        elif cards[1] == cards[2]:
            result = self.cardController.getByName(cards[0])
        elif cards[0] == cards[2]:
            result = self.cardController.getByName(cards[1])
        elif attribute == 1:
            result, winner = self.getWinnerByType(cards[0], cards[1], cards[2])
        elif attribute == 2:
            result, winner = self.getWinnerByFirstAppearance(cards[0], cards[1], cards[2])
        elif attribute == 3:
            result, winner = self.getWinnerByLevelOfFear(cards[0], cards[1], cards[2])
        elif attribute == 4:
            result, winner = self.getWinnerBySize(cards[0], cards[1], cards[2])
        elif attribute == 5:
            result, winner = self.getWinnerByDanger(cards[0], cards[1], cards[2])
        elif attribute == 6:
            result, winner = self.getWinnerByRarity(cards[0], cards[1], cards[2])
        
        return winner+1, result

    def getWinnerByType(self, cardName1, cardName2, cardName3):
        card1 = self.cardController.getByName(cardName1)
        card2 = self.cardController.getByName(cardName2)
        card3 = self.cardController.getByName(cardName3)
        cards = [card1, card2, card3]

        elements = [sub[2] for sub in cards]
        indices = [type.index(element) for element in elements]
        winner = indices.index(max(indices))

        return cards[winner], winner

    def getWinnerByFirstAppearance(self, cardName1, cardName2, cardName3):
        card1 = self.cardController.getByName(cardName1)
        card2 = self.cardController.getByName(cardName2)
        card3 = self.cardController.getByName(cardName3)
        cards = [card1, card2, card3]
        index_of_min = min(cards, key=lambda x: x[3])
        occurencies = cards.count(cards[index_of_min][3])
        if occurencies == 1:
            return cards[index_of_min], index_of_min
        else:
            print("Vamos para o desempate")
            self.getWinnerByRarity(cardName1, cardName2, cardName3)

    def getWinnerByLevelOfFear(self, cardName1, cardName2, cardName3):
        card1 = self.cardController.getByName(cardName1)
        card2 = self.cardController.getByName(cardName2)
        card3 = self.cardController.getByName(cardName3)
        cards = [card1, card2, card3]

        elements = [sub[4] for sub in cards]
        indices = [self.fear.index(element) for element in elements]
        indicesSorted = sorted(indices, key=lambda item: item, reverse=True)
        undraw = 0 
        for i in cards:
            if indicesSorted == i:
                undraw = undraw + 1
        if undraw == 1:
            winner = indices.index(max(indices))
            return cards[winner], winner
        else:
            print("Vamos para o desempate")
            self.getWinnerByDanger(cardName1, cardName2, cardName3)

    def getWinnerBySize(self, cardName1, cardName2, cardName3):
        card1 = self.cardController.getByName(cardName1)
        card2 = self.cardController.getByName(cardName2)
        card3 = self.cardController.getByName(cardName3)
        cards = [card1, card2, card3]
        index_of_min = min(cards, key=lambda x: x[5])
        occurencies = cards.count(cards[index_of_min][5])
        if occurencies == 1:
            return cards[index_of_min], index_of_min
        else:
            print("Vamos para o desempate")
            self.getWinnerByLevelOfFear(cardName1, cardName2, cardName3)

    def getWinnerByDanger(self, cardName1, cardName2, cardName3):
        card1 = self.cardController.getByName(cardName1)
        card2 = self.cardController.getByName(cardName2)
        card3 = self.cardController.getByName(cardName3)
        cards = [card1, card2, card3]

        elements = [sub[6] for sub in cards]
        indices = [self.dangerous.index(element) for element in elements]
        indicesSorted = sorted(indices, key=lambda item: item, reverse=True)
        undraw = 0 
        for i in cards:
            if indicesSorted == i:
                undraw = undraw + 1
        if undraw == 1:
            winner = indices.index(max(indices))
            return cards[winner], winner
        else:
            print("Vamos para o desempate")
            self.getWinnerByFirstAppearance(cardName1, cardName2, cardName3)

    def getWinnerByRarity(self, cardName1, cardName2, cardName3):
        card1 = self.cardController.getByName(cardName1)
        card2 = self.cardController.getByName(cardName2)
        card3 = self.cardController.getByName(cardName3)
        cards = [card1, card2, card3]

        elements = [sub[7] for sub in cards]
        indices = [self.rare.index(element) for element in elements]
        indicesSorted = sorted(indices, key=lambda item: item, reverse=True)
        undraw = 0 
        for i in cards:
            if indicesSorted == i:
                undraw = undraw + 1
        if undraw == 1:
            winner = indices.index(max(indices))
            return cards[winner], winner
        else:
            print("Vamos para o desempate")
            self.getWinnerByDanger(cardName1, cardName2, cardName3)
