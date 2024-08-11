from datetime import datetime
import CardController
import DeckController
import sqlite3
conn = sqlite3.connect('../database/cryptid.db')
cursor = conn.cursor()

def getAll():
    cursor.execute('SELECT * FROM match')
    rows = cursor.fetchall()
    conn.commit()
    
    return rows


def getById(matchId):
    cursor.execute('SELECT * FROM match WHERE match_id = ?', (matchId,))
    rows = cursor.fetchall()
    conn.commit()
    return rows

def getByAmountWinsByDeck(deckId):
    cursor.execute('SELECT COUNT(*) FROM match WHERE winner_deck_id = ?', (deckId,))
    rows = cursor.fetchall()
    conn.commit()
    return rows

def getAmountWinsByUser(userId):
    userDecksList = DeckController.getDeckByUser(userId)
    userDecks = [decks[0]for decks in userDecksList]
    amount = 0
    for i in userDecks:
        amountByDeckList = getByAmountWinsByDeck(i)
        amountDeck = [quantity[0]for quantity in amountByDeckList][0]
        amount = amount + amountDeck
    print("Vitórias do usuario: ",amount)
    return amount

def insert(match):
    try:
        cursor.execute('''
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

def RoundResult(card1, card2, card3, attribute):
    if attribute == 1:
        getWinnerByType(card1, card2, card3)
    elif attribute == 2:
        getWinnerByFirstAppearance(card1, card2, card3)
    elif attribute == 3:
        getWinnerByLevelOfFear(card1, card2, card3)
    elif attribute == 4:
        getWinnerBySize(card1, card2, card3)
    elif attribute == 5:
        getWinnerByDanger(card1, card2, card3)
    elif attribute == 6:
        getWinnerByRarity(card1, card2, card3)
    

def getWinnerByType(card1, card2, card3):
    card1 = CardController.getByName(card1)
    card2 = CardController.getByName(card2)
    card3 = CardController.getByName(card3)
    cards = [card1, card2, card3]

    elements = [sub[2] for sub in cards]
    indices = [type.index(element) for element in elements]
    winner = indices.index(max(indices))

    print("vencedor: ", cards[winner])
    return cards[winner]

def getWinnerByFirstAppearance(card1, card2, card3):
    card1 = CardController.getByName(card1)
    card2 = CardController.getByName(card2)
    card3 = CardController.getByName(card3)
    cards = [card1, card2, card3]

    # elements = [sub[3] for sub in cards]
    # indices = [fear.index(element) for element in elements]
    # winner = indices.index(max(indices))

    # print("vencedor: ", cards[winner])
    # return cards[winner]

def getWinnerByLevelOfFear(cardName1, cardName2, cardName3):
    card1 = CardController.getByName(cardName1)
    card2 = CardController.getByName(cardName2)
    card3 = CardController.getByName(cardName3)
    cards = [card1, card2, card3]

    elements = [sub[4] for sub in cards]
    indices = [fear.index(element) for element in elements]
    winner = indices.index(max(indices))

    print("vencedor: ", cards[winner])
    return cards[winner]

def getWinnerBySize(card1, card2, card3):
    card1 = CardController.getByName(card1)
    card2 = CardController.getByName(card2)
    card3 = CardController.getByName(card3)
    cards = [card1, card2, card3]
    # elements = [sub[4] for sub in cards]
    # indices = [fear.index(element) for element in elements]
    # winner = indices.index(max(indices))

    # print("vencedor: ", cards[winner])
    # return cards[winner]

def getWinnerByDanger(card1, card2, card3):
    card1 = CardController.getByName(card1)
    card2 = CardController.getByName(card2)
    card3 = CardController.getByName(card3)
    cards = [card1, card2, card3]

    elements = [sub[6] for sub in cards]
    indices = [dangerous.index(element) for element in elements]
    winner = indices.index(max(indices))
    print("indices: ",indices)
    print("vencedor: ", cards[winner])
    return cards[winner]

def getWinnerByRarity(card1, card2, card3):
    card1 = CardController.getByName(card1)
    card2 = CardController.getByName(card2)
    card3 = CardController.getByName(card3)
    cards = [card1, card2, card3]

    elements = [sub[7] for sub in cards]
    indices = [rare.index(element) for element in elements]
    winner = indices.index(max(indices))

    print("vencedor: ", cards[winner])
    return cards[winner]

def main():
    print("Escolha uma opção:")
    print("1) GetAll")
    print("2) RoundResult")
    print("3) getAmountWinsByUser")
    escolha = int(input())

    if escolha == 1:
        matches = getAll()
        for match in matches:
            print(match)
    elif escolha == 2:
        print("Escolha o atributo")
        print("1) Type")
        print("2) First Appearance")
        print("3) Level of fear")
        print("4) Size")
        print("5) Danger")
        print("6) Rarity")
        attribute = int(input())
        RoundResult("Yeti","Bruxa","Slenderman",attribute)
    elif escolha == 3:
        userId = input('digte o userId: ')
        matches = getAmountWinsByUser(userId)



if __name__ == "__main__":
    main()
