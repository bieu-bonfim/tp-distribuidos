from datetime import datetime
import sqlite3
conn = sqlite3.connect('../database/cryptid.db')
cursor = conn.cursor()

def getAll():
    cursor.execute('SELECT * FROM deck')
    rows = cursor.fetchall()
    conn.commit()
    return rows
def getById(deckId):
    cursor.execute('SELECT * FROM deck WHERE deck_id = ?', (deckId,))
    rows = cursor.fetchall()
    conn.commit()
    return rows

def getAmountDeckByUser(userId):
    cursor.execute('SELECT COUNT(*) FROM deck WHERE user_id = ?', (userId,))
    rows = cursor.fetchall()
    conn.commit()
    return rows

def getDeckByUser(userId):
    cursor.execute('SELECT deck_id FROM deck WHERE user_id = ?', (userId,))
    rows = cursor.fetchall()
    conn.commit()
    return rows

def insert(deck):
    try:
        amountDecks = getAmountDeckByUser(deck[2])
        amount = [quantity[0]for quantity in amountDecks][0]
        if(amount <= 3):
            cursor.execute('''
                INSERT INTO deck (valid, name, user_id) VALUES (?, ?, ?)
            ''', deck)
            conn.commit()
            print("Deck inserido com sucesso!")
        else:
            print("O usuário pode ter no máximo 3 Decks")
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
        deck = getById(deckId)
        print(deck)

    elif escolha == 3:
        valid = input('digte o valid: ')
        name = input('digte o name: ')
        userId = input('digte a userId: ')
        deck = (valid, name, userId)
        insert(deck)
        print(deck)
    
    elif escolha == 4:
        deckId = int(input('digte o id: '))
        deck = delete(deckId)

if __name__ == "__main__":
    main()
