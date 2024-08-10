from datetime import datetime
import sqlite3
import UserCardsController
import CardController
conn = sqlite3.connect('../database/cryptid.db')
cursor = conn.cursor()

def getAll():
    cursor.execute('SELECT * FROM deck_cards')
    rows = cursor.fetchall()
    conn.commit()
    conn.close()
    return rows

def getCardByDeck(deckId):
    cursor.execute('SELECT c.* FROM deck_cards dc INNER JOIN card c on dc.card_id = c.card_id WHERE deck_id = ?', (deckId,))
    rows = cursor.fetchall()
    conn.commit()
    conn.close()
    return rows

def insert(deck_card, userId):
    try:
        userCards = UserCardsController.getCardByUser(userId)
        print("Cartas do bija: ",userCards)
        print("deck card [1]", deck_card[1])
        card = CardController.getById(deck_card[1])
        print ("Carta: ",card)
        if card in userCards:
            cursor.execute('''
                INSERT INTO deck_cards (deck_id, card_id, quantity) VALUES (?, ?, ?)
            ''', deck_card)
            conn.commit()
            conn.close()
        else: 
            print("usuario nao tem a carta")
    except Exception as e:
        print('Não foi possível inserir o deck: ',e)
        
    
def update(self, username, email, password, createAt, deletedAt):
    self.username = username
    self.email = email
    self.password = password
    self.createAt = createAt
    self.deletedAt = deletedAt
    
def delete(deckId):
    currentDate = datetime.now()
    cursor.execute('''
    UPDATE deck
    SET deleted_at = ?
    WHERE deck_id = ?
    ''', (currentDate, deckId))
    conn.commit()
    conn.close()

def main():
    print("Escolha uma opção:")
    print("1) GetAll")
    print("2) GetById")
    print("3) Insert")
    print("4) Delete")
    escolha = int(input())

    if escolha == 1:
        decks = getAll()
        for deck in decks:
            print(deck)

    elif escolha == 2:
        deckId = int(input('digte o id: '))
        deck = getCardByDeck(deckId)
        print(deck)

    elif escolha == 3:
        user = input('digite o id do usuario: ')
        deck = input('digte o id do deck: ')
        carta = input('digte o id da carta: ')
        quantidade = input('digte a quantidade: ')
        deckCard = (deck, carta, quantidade)
        insert(deckCard, user)
        print('inserido com sucesso')
        print(deckCard)
    
    elif escolha == 4:
        deckId = int(input('digte o id: '))
        deck = delete(deckId)

if __name__ == "__main__":
    main()
