from datetime import datetime
import random
import sqlite3
conn = sqlite3.connect('../database/cryptid.db')
cursor = conn.cursor()

def getAll():
    cursor.execute('SELECT * FROM user_cards')
    rows = cursor.fetchall()
    conn.commit()
    conn.close()
    return rows

def getCardByUser(userId):
    cursor.execute('SELECT c.name FROM user_cards uc INNER JOIN card c on uc.card_id = c.card_id WHERE user_id = ?', (userId,))
    rows = cursor.fetchall()
    conn.commit()
    conn.close()
    return rows

def buyBooster(userId):
    numeros = [random.randint(1, 27),random.randint(1, 27),random.randint(1, 27)]
    print("numeros: ", numeros)
    userCard1 = (userId, numeros[0], 1)
    userCard2 = (userId, numeros[1], 1)
    userCard3 = (userId, numeros[2], 1)
    insert(userCard1)
    insert(userCard2)
    insert(userCard3)

def insert(user_card):
    try:
        cursor.execute('''
            INSERT INTO user_cards (user_id, card_id, quantity) VALUES (?, ?, ?)
        ''', user_card)
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
        deck = getCardByUser(deckId)
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
        print(userCard)

if __name__ == "__main__":
    main()
