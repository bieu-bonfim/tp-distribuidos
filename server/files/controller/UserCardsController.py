from datetime import datetime
import random
import CardController
import sqlite3
conn = sqlite3.connect('../database/cryptid.db')
cursor = conn.cursor()

def getAll():
    cursor.execute('SELECT * FROM user_cards')
    rows = cursor.fetchall()
    conn.commit()

    return rows

def getCardNameByUser(userId):
    cursor.execute('SELECT c.name FROM user_cards uc INNER JOIN card c on uc.card_id = c.card_id WHERE user_id = ?', (userId,))
    rows = cursor.fetchall()
    conn.commit()

    return rows

def getCardIdByUser(userId):
    cursor.execute('SELECT c.card_id FROM user_cards uc INNER JOIN card c on uc.card_id = c.card_id WHERE user_id = ?', (userId,))
    rows = cursor.fetchall()
    conn.commit()

    return rows

def getQuantityCardByUser(userId, cardId):
    cursor.execute('SELECT uc.quantity FROM user_cards uc WHERE user_id = ? and card_id = ?', (userId, cardId))
    rows = cursor.fetchall()
    conn.commit()
    return rows

def buyBooster(userId):
    cardIdBooster = random.sample(range(1, 28), 3)
    userCardsTuple = getCardIdByUser(userId)
    idCardUser = [item[0] for item in userCardsTuple]
    for cardId in cardIdBooster:
        if cardId not in idCardUser:
            userCard = (userId, cardId, 1)
            insert(userCard)
            print("Carta nova inserida com sucesso, você ganhou um: ", CardController.getNameById(cardId))
        else:
            quantity = getQuantityCardByUser(userId, cardId)
            newQuantity = [q[0]for q in quantity][0] + 1
            userCard = (userId, cardId, newQuantity)
            updateQuantityCard(userCard)
            print("Você já possuía esta carta, agora você tem ", newQuantity," ", CardController.getNameById(cardId))



def insert(user_card):
    try:
        cursor.execute('''
            INSERT INTO user_cards (user_id, card_id, quantity) VALUES (?, ?, ?)
        ''', user_card)
        conn.commit()
    except Exception as e:
        print('Não foi possível inserir o deck: ',e)
        
def updateQuantityCard(userCard):
    try:
        cursor.execute('''
        UPDATE user_cards
        SET quantity = ?
        WHERE user_id = ? and card_id = ?
        ''', (userCard))
        conn.commit()
    except Exception as e:
        print('Não foi possível inserir o deck: ',e)


def main():
    print("Escolha uma opção:")
    print("1) GetAll")
    print("2) GetCardByUser")
    print("3) Insert")
    print("4) BuyBooster")
    escolha = int(input())

    if escolha == 1:
        decks = getAll()
        for deck in decks:
            print(deck)

    elif escolha == 2:
        deckId = int(input('digte o id: '))
        deck = getCardNameByUser(deckId)
        print(deck)

    elif escolha == 3:
        deck = input('digte o id do usuario: ')
        carta = input('digte o id da carta: ') 
        quantidade = input('digte a quantidade: ')
        deckCard = (deck, carta, quantidade)
        insert(deckCard)
        print('inserido com sucesso')
        print(deckCard)
    elif escolha == 4:
        userId = int(input('digte o id: '))
        userCard = buyBooster(userId)
        #print(userCard)

if __name__ == "__main__":
    main()
