from datetime import datetime
import sqlite3
conn = sqlite3.connect('cryptid.db')
cursor = conn.cursor()

def getAll():
    cursor.execute('SELECT * FROM card')
    rows = cursor.fetchall()
    conn.commit()
    conn.close()
    return rows

def getById(cardId):
    cursor.execute('SELECT * FROM card WHERE card_id = ?', (cardId,))
    rows = cursor.fetchall()
    conn.commit()
    conn.close()
    return rows
def insert(card):
    try:
        cursor.execute('''
            INSERT INTO card (name, type, first_appearance, level_of_fear, size, danger, rarity) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', card)
        conn.commit()
        conn.close()
    except Exception as e:
        print('Não foi possível inserir a carta: ',e)
        
    
    
def delete(cardId):
    currentDate = datetime.now()
    cursor.execute('''
    UPDATE card
    SET deleted_at = ?
    WHERE card_id = ?
    ''', (currentDate, cardId))
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
        cards = getAll()
        for card in cards:
            print(card)

    elif escolha == 2:
        cardId = int(input('digte o id: '))
        card = getById(cardId)
        print(card)

    elif escolha == 3:
        name = input('digte o name: ')
        type = input('digte o type: ')
        firstAppearance = input('digte o firstAppearance: ')
        levelOfFear = input('digte o levelOfFear: ')
        size = input('digte o size: ')
        danger = input('digte o danger: ')
        rarity = input('digte a rarity: ')
        card = (name, type, firstAppearance, levelOfFear, size, danger, rarity)
        insert(card)
        print('carta inserido com sucesso')
        print(card)
    
    elif escolha == 4:
        cardId = int(input('digte o id: '))
        card = delete(cardId)

if __name__ == "__main__":
    main()
