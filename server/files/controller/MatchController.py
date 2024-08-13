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
        "Fique Atento",
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
            return 0, -1
        elif cards[0] == cards[1]:
            result = self.cardController.getByName(cards[2])
            winner = 2
        elif cards[1] == cards[2]:
            result = self.cardController.getByName(cards[0])
            winner = 0
        elif cards[0] == cards[2]:
            result = self.cardController.getByName(cards[1])
            winner = 1
        elif attribute == "Tipo":
            result, winner = self.getWinnerByType(cards[0], cards[1], cards[2])
        elif attribute == "Avistamento":
            result, winner = self.getWinnerByFirstAppearance(cards[0], cards[1], cards[2])
        elif attribute == "Medo":
            result, winner = self.getWinnerByLevelOfFear(cards[0], cards[1], cards[2])
        elif attribute == "Tamanho":
            print('tamanho da carta')
            result, winner = self.getWinnerBySize(cards[0], cards[1], cards[2])
        elif attribute == "Perigo":
            result, winner = self.getWinnerByDanger(cards[0], cards[1], cards[2])
        elif attribute == "Raridade":
            result, winner = self.getWinnerByRarity(cards[0], cards[1], cards[2])
        
        return result, winner

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
        min_date = min(cards, key=lambda x: x[3])
        
        index_of_min = cards.index(min_date)
        
        occurencies = sum(1 for card in cards if card[3] == min_date[3])
        
        if occurencies == 1:
            return cards[min_date], index_of_min
        else:
            print("Vamos para o desempate")
            self.getWinnerByRarity(cardName1, cardName2, cardName3)

    def getWinnerByLevelOfFear(self, cardName1, cardName2, cardName3):
        card1 = self.cardController.getByName(cardName1)
        card2 = self.cardController.getByName(cardName2)
        card3 = self.cardController.getByName(cardName3)
        cards = [card1, card2, card3]

        fear_map = {level: i for i, level in enumerate(self.fear)}
        
        max_fear = max(cards, key=lambda x: fear_map[x[4]])
        
        index_of_max = cards.index(max_fear)
        
        max_fear_level = fear_map[max_fear[4]]
        
        draw_count = sum(1 for card in cards if fear_map[card[4]] == max_fear_level)

        if draw_count == 1:
            return cards[index_of_max], index_of_max
        else:
            print("Vamos para o desempate")
            self.getWinnerByDanger(cardName1, cardName2, cardName3)

    def getWinnerBySize(self, cardName1, cardName2, cardName3):
        card1 = self.cardController.getByName(cardName1)
        card2 = self.cardController.getByName(cardName2)
        card3 = self.cardController.getByName(cardName3)
        cards = [card1, card2, card3]
        max_size = max(cards, key=lambda x: x[5])
        
        index_of_max = cards.index(max_size)
        
        occurencies = sum(1 for card in cards if card[5] == max_size[5])
        
        if occurencies == 1:
            return cards[index_of_max], index_of_max
        else:
            print("Vamos para o desempate")
            self.getWinnerByLevelOfFear(cardName1, cardName2, cardName3)

    def getWinnerByDanger(self, cardName1, cardName2, cardName3):
        card1 = self.cardController.getByName(cardName1)
        card2 = self.cardController.getByName(cardName2)
        card3 = self.cardController.getByName(cardName3)
        cards = [card1, card2, card3]

        danger_map = {level: i for i, level in enumerate(self.dangerous)}
        
        max_danger = max(cards, key=lambda x: danger_map[x[6]])
        
        index_of_max = cards.index(max_danger)
        
        max_danger_level = danger_map[max_danger[6]]
        
        draw_count = sum(1 for card in cards if danger_map[card[6]] == max_danger_level)

        if draw_count == 1:
            return cards[index_of_max], index_of_max
        else:
            print("Vamos para o desempate!")
            self.getWinnerByFirstAppearance(cardName1, cardName2, cardName3)

    def getWinnerByRarity(self, cardName1, cardName2, cardName3):
        card1 = self.cardController.getByName(cardName1)
        card2 = self.cardController.getByName(cardName2)
        card3 = self.cardController.getByName(cardName3)
        cards = [card1, card2, card3]

        rarity_map = {level: i for i, level in enumerate(self.dangerous)}
        
        max_rarity = max(cards, key=lambda x: rarity_map[x[7]])
        
        index_of_max = cards.index(max_rarity)
        
        max_rarity_level = rarity_map[max_rarity[7]]
        
        draw_count = sum(1 for card in cards if rarity_map[card[7]] == max_rarity_level)

        if draw_count == 1:
            return cards[index_of_max], index_of_max
        else:
            print("Vamos para o desempate")
            self.getWinnerByDanger(cardName1, cardName2, cardName3)
