from datetime import datetime
import CardController
import DeckController
import sqlite3
conn = sqlite3.connect('../database/cryptid.db')
cursor = conn.cursor()
class MatchController:
    def getAll(self):
        self.cursor.execute('SELECT * FROM match')
        rows = self.cursor.fetchall()
        conn.commit()
        
        return rows


    def getById(self, matchId):
        self.cursor.execute('SELECT * FROM match WHERE match_id = ?', (matchId,))
        rows = self.cursor.fetchall()
        conn.commit()
        return rows

    def getByAmountWinsByDeck(self, deckId):
        self.cursor.execute('SELECT COUNT(*) FROM match WHERE winner_deck_id = ?', (deckId,))
        rows = self.cursor.fetchall()
        conn.commit()
        return rows

    def getAmountWinsByUser(self, userId):
        userDecksList = DeckController.getDeckByUser(userId)
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

    def RoundResult(self, card1, card2, card3, attribute):
        if attribute == 1:
            self.getWinnerByType(card1, card2, card3)
        elif attribute == 2:
            self.getWinnerByFirstAppearance(card1, card2, card3)
        elif attribute == 3:
            self.getWinnerByLevelOfFear(card1, card2, card3)
        elif attribute == 4:
            self.getWinnerBySize(card1, card2, card3)
        elif attribute == 5:
            self.getWinnerByDanger(card1, card2, card3)
        elif attribute == 6:
            self.getWinnerByRarity(card1, card2, card3)
        

    def getWinnerByType(self, card1, card2, card3):
        card1 = CardController.getByName(card1)
        card2 = CardController.getByName(card2)
        card3 = CardController.getByName(card3)
        cards = [card1, card2, card3]

        elements = [sub[2] for sub in cards]
        indices = [type.index(element) for element in elements]
        winner = indices.index(max(indices))

        print("vencedor: ", cards[winner])
        return cards[winner]

    def getWinnerByFirstAppearance(self, card1, card2, card3):
        card1 = CardController.getByName(card1)
        card2 = CardController.getByName(card2)
        card3 = CardController.getByName(card3)
        cardList = [card1, card2, card3]

        cardListSorted = sorted(cardList, key=lambda item: item[3])
        print("vencedor: ",cardListSorted[0])
        return cardListSorted[0]

    def getWinnerByLevelOfFear(self, cardName1, cardName2, cardName3):
        card1 = CardController.getByName(cardName1)
        card2 = CardController.getByName(cardName2)
        card3 = CardController.getByName(cardName3)
        cards = [card1, card2, card3]

        elements = [sub[4] for sub in cards]
        indices = [self.fear.index(element) for element in elements]
        winner = indices.index(max(indices))

        print("vencedor: ", cards[winner])
        return cards[winner]

    def getWinnerBySize(self, card1, card2, card3):
        card1 = CardController.getByName(card1)
        card2 = CardController.getByName(card2)
        card3 = CardController.getByName(card3)
        cardList = [card1, card2, card3]
        cardListSorted = sorted(cardList, key=lambda item: item[5], reverse=True)
        print("vencedor: ",cardListSorted[0])
        return cardListSorted[0]

    def getWinnerByDanger(self, card1, card2, card3):
        card1 = CardController.getByName(card1)
        card2 = CardController.getByName(card2)
        card3 = CardController.getByName(card3)
        cards = [card1, card2, card3]

        elements = [sub[6] for sub in cards]
        indices = [self.dangerous.index(element) for element in elements]
        winner = indices.index(max(indices))
        print("indices: ",indices)
        print("vencedor: ", cards[winner])
        return cards[winner]

    def getWinnerByRarity(self, card1, card2, card3):
        card1 = CardController.getByName(card1)
        card2 = CardController.getByName(card2)
        card3 = CardController.getByName(card3)
        cards = [card1, card2, card3]

        elements = [sub[7] for sub in cards]
        indices = [self.rare.index(element) for element in elements]
        winner = indices.index(max(indices))

        print("vencedor: ", cards[winner])
        return cards[winner]
