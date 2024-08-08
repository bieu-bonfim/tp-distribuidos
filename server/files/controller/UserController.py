from datetime import datetime
import sqlite3
conn = sqlite3.connect('cryptid.db')
cursor = conn.cursor()

def getAll():
    cursor.execute('SELECT * FROM user')
    rows = cursor.fetchall()
    conn.commit()
    conn.close()
    return rows
def getById(userId):
    cursor.execute('SELECT * FROM user WHERE user_id = ?', (userId,))
    rows = cursor.fetchall()
    conn.commit()
    conn.close()
    return rows
def insert(user):
    try:
        cursor.execute('''
            INSERT INTO user (username, email, password, create_at) VALUES (?, ?, ?, ?)
        ''', user)
        conn.commit()
        conn.close()
    except Exception as e:
        print('Não foi possível inserir usuário: ',e)
        
    
def update(self, username, email, password, createAt, deletedAt):
    self.username = username
    self.email = email
    self.password = password
    self.createAt = createAt
    self.deletedAt = deletedAt
    
def delete(userId):
    currentDate = datetime.now()
    cursor.execute('''
    UPDATE user
    SET deleted_at = ?
    WHERE user_id = ?
    ''', (currentDate, userId))
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
        users = getAll()
        for user in users:
            print(user)

    elif escolha == 2:
        userId = int(input('digte o id: '))
        user = getById(userId)
        print(user)

    elif escolha == 3:
        username = input('digte o username: ')
        email = input('digte o email: ')
        senha = input('digte a senha: ')
        dataAtual = datetime.now()
        user = (username ,email, senha, dataAtual)
        insert(user)
        print('usuário inserido com sucesso')
        print(user)
    
    elif escolha == 4:
        userId = int(input('digte o id: '))
        user = delete(userId)

if __name__ == "__main__":
    main()
